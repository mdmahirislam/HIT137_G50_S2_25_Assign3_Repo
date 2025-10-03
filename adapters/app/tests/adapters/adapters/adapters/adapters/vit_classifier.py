from PIL import Image
from transformers import pipeline
from .base import ModelAdapter
from .mixins import LoggingMixin

# ---------- decorators (multiple) ----------
def ensure_image_path(func):
    """Decorator to ensure an image path is provided."""
    def wrapper(self, image_path: str, *args, **kwargs):
        if not image_path or not str(image_path).strip():
            raise ValueError("Please choose an image file first.")
        return func(self, image_path, *args, **kwargs)
    return wrapper

def topk_bounds(func):
    """Decorator to keep top_k in a sensible range."""
    def wrapper(self, image_path: str, *args, top_k: int = 3, **kwargs):
        k = 1 if top_k < 1 else (10 if top_k > 10 else top_k)
        return func(self, image_path, *args, top_k=k, **kwargs)
    return wrapper

def catch_errors(func):
    """Decorator to provide a cleaner error surface to the GUI."""
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Image classification failed: {e}") from e
    return wrapper
# ------------------------------------------


class VitImageClassifier(LoggingMixin, ModelAdapter):
    """
    Lightweight Transformers image classifier (ViT).
    Demonstrates multiple inheritance (LoggingMixin + ModelAdapter),
    encapsulation (_pipe/_model), and method overriding (load/run).
    """
    def __init__(self, model_name: str = "google/vit-base-patch16-224"):
        super().__init__(display_name="Image → Classification (ViT)")
        self.model_name = model_name
        self._pipe = None

    # --- overriding ---
    def load(self) -> None:
        # CPU is fine for this model.
        self._pipe = pipeline("image-classification", model=self.model_name)
        self._model = self._pipe.model

    @catch_errors
    @topk_bounds
    @ensure_image_path       # multiple decorators (stacked)
    def run(self, image_path: str, top_k: int = 3):
        self.ensure_loaded()
        end_timer = self._time_block()  # from LoggingMixin
        try:
            img = Image.open(image_path).convert("RGB")
            preds = self._pipe(img, top_k=top_k)
            return [{"label": p["label"], "score": float(p["score"])} for p in preds]
        finally:
            end_timer()

    # helper used by GUI
    def brief_info(self) -> str:
        self.ensure_loaded()
        lines = [
            f"Model: {self.model_name}",
            "Task: Image Classification",
            "Library: Transformers (pipeline)",
        ]
        t = self.last_run_seconds()
        if t is not None:
            lines.append(f"Last inference time: {t:.3f} s")
        return "\n".join(lines)
