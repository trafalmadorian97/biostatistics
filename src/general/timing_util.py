import contextlib
import time


@contextlib.contextmanager
def time_this(name: str):
    print(f"Starting {name}")
    start = time.perf_counter()
    yield None
    end = time.perf_counter()
    print(f"{name} took {end - start}")
