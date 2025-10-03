from abc import ABC, abstractmethod

class ModelAdapter(ABC):
    """
    Abstract base for all AI model adapters.
    Encapsulation via _loaded/_model and a unified interface.
    """
    def __init__(self, display_name: str = "Model"):
        self._loaded = False
        self._model = None
        self.display_name = display_name

    @abstractmethod
    def load(self) -> None:
        """Load underlying model/pipeline exactly once."""
        ...

    @abstractmethod
    def run(self, *args, **kwargs):
        """Run inference and return a Python object (dict/list/str)."""
        ...

    def ensure_loaded(self) -> None:
        """Public guard that lazily ensures 'load' only runs once."""
        if not self._loaded:
            self.load()
            self._loaded = True
