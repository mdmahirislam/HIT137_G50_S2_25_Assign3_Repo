import time

class LoggingMixin:
    """Tiny mixin for optional timing/logging. Demonstrates multiple inheritance."""
    _last_run_secs: float | None = None

    def _time_block(self):
        start = time.perf_counter()
        def end():
            self._last_run_secs = time.perf_counter() - start
        return end

    def last_run_seconds(self) -> float | None:
        return self._last_run_secs
