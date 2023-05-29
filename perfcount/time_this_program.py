import time
import inspect
import atexit
# run the code here to time the module that imported this from the time of import to the exit of the interpreter

__all__ = []

_frame = inspect.currentframe().f_back.f_back.f_back.f_back.f_back.f_back
_module = inspect.getmodule(_frame).__name__
_file = inspect.getfile(_frame)

atexit.register(lambda: print(f"perftest: the module {_module!r} from file {_file!r} took {time.perf_counter_ns()-_start}ns to run"))

_start = time.perf_counter_ns()