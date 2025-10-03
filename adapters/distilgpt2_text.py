from transformers import pipeline
from .base import ModelAdapter
from .mixins import LoggingMixin

# --------- decorators (multiple) ----------
def ensure_prompt(func):
    """Require a non-empty prompt."""
    def wrapper(self, prompt: str, *args, **kwargs):
        if not prompt or not str(prompt).strip():
            raise ValueError("Please enter some text in the prompt box.")
        return func(self, prompt, *args, **kwargs)
    return wrapper

def length_bounds(func):
    """Clamp max_new_tokens to a sensible range."""
    def wrapper(self, prompt: str, *args, max_new_tokens: int = 64, **kwargs):
        n = 1 if max_new_tokens < 1 else (256 if max_new_tokens > 256 else max_new_tokens)
        return func(self, prompt, *args, max_new_tokens=n, **kwargs)
    return wrapper

def sampling_bounds(func):
    """Clamp temperature/top_p to safe ranges."""
    def wrapper(self, prompt: str, *args, temperature: float = 0.7, top_p: float = 0.9, **kwargs):
        t = 0.1 if temperature < 0.1 else (2.0 if temperature > 2.0 else temperature)
        p = 0.1 if top_p < 0.1 else (1.0 if top_p > 1.0 else top_p)
        return func(self, prompt, *args, temperature=t, top_p=p, **kwargs)
    return wrapper

def catch_errors(func):
    """Normalize errors for the GUI."""
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Text generation failed: {e}") from e
    return wrapper
# ------------------------------------------


class DistilGPT2TextGen(LoggingMixin, ModelAdapter):
    """
    Lightweight text generator using Transformers pipeline.
    Model: 'distilgpt2' (small, widely used, CPU-friendly).
    Demonstrates multiple inheritance, encapsulation, overriding, decorators.
    """
    def __init__(self, model_name: str = "distilgpt2"):
        super().__init__(display_name="Text → Generation (DistilGPT2)")
        self.model_name = model_name
        self._pipe = None

    # --- overriding ---
    def load(self) -> None:
        # CPU-only is fine; no extra heavy libs required.
        self._pipe = pipeline("text-generation", model=self.model_name)
        self._model = self._pipe.model

    @catch_errors
    @sampling_bounds
    @length_bounds
    @ensure_prompt
    def run(self, prompt: str, max_new_tokens: int = 64, temperature: float = 0.7, top_p: float = 0.9, do_sample: bool = True):
        self.ensure_loaded()
        end_timer = self._time_block()
        try:
            out = self._pipe(
                prompt,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=do_sample,
                # repetition_penalty can help a bit; keep default for simplicity
            )
            # pipeline returns a list of dicts with 'generated_text'
            return out[0]["generated_text"]
        finally:
            end_timer()

    # helper used by GUI
    def brief_info(self) -> str:
        self.ensure_loaded()
        lines = [
            f"Model: {self.model_name}",
            "Task: Text Generation",
            "Library: Transformers (pipeline)",
        ]
        t = self.last_run_seconds()
        if t is not None:
            lines.append(f"Last inference time: {t:.3f} s")
        return "\n".join(lines)
