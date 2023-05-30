"""Useful Python library for performance testing that contains multiple function decorators"""

__version__ = "1.0.1"

import time
import threading
import warnings
import traceback
import unittest.mock
import contextlib
import inspect
from types import FunctionType

def perf(*, verbose=False, suppress_output=False):
	"""Print out the performance data of the function in seconds"""

	def wrapper(func: FunctionType):
		def inner(*args, **kwargs):

			if suppress_output:
				with contextlib.redirect_stdout(unittest.mock.Mock()):
					start = time.perf_counter()
					res = func(*args, **kwargs)
					length = time.perf_counter() - start
			else:
				start = time.perf_counter()
				res = func(*args, **kwargs)
				length = time.perf_counter() - start

			if verbose:
				frame = inspect.currentframe().f_back
				line = traceback.format_list(traceback.extract_stack(limit=2))[0].split('\n')[1].strip()
				
				print(f"perftest:\n\t{repr(line)}\n\t\ton line {inspect.getlineno(frame)}\n\t\tin file {inspect.getfile(frame)}\n\ttook {length} secs")
				return res

			print(f"perftest: {func.__name__} took {length} secs")

			return res
		
		return inner
		
	return wrapper

def perf_ns(*, verbose=False, suppress_output=False):
	"""Print out the performance data of the function in nanoseconds"""

	def wrapper(func: FunctionType):
		def inner(*args, **kwargs):

			if suppress_output:
				with contextlib.redirect_stdout(unittest.mock.Mock()): 
					start = time.perf_counter_ns()
					res = func(*args, **kwargs)
					length = time.perf_counter_ns()-start
			else:
				start = time.perf_counter_ns()
				res = func(*args, **kwargs)
				length = time.perf_counter_ns()-start

			if verbose:
				frame = inspect.currentframe().f_back
				line = traceback.format_list(traceback.extract_stack(limit=2))[0].split('\n')[1].strip()
				
				print(f"perftest:\n\t{repr(line)}\n\t\ton line {inspect.getlineno(frame)}\n\t\tin file {inspect.getfile(frame)}\n\ttook {length}ns")
				return res

			print(f"perftest: {func.__name__} took {length}ns")

			return res

		return inner
	
	return wrapper

def shouldtake(nanoseconds: int=None, milliseconds: int=None, seconds: int=None, *, verbose=False, suppress_output=False, throw=False, warn=False):
	"""Make sure that a function only takes under a certain amount of time to run (using throw=True or warn=True)"""

	if (warn and throw) or ((not warn) and (not throw)): # both true or both false
		raise ValueError(
			"Either `warn` or `throw` should be set; both cannot be set, at least one must be set"
		)
	
	measurements = (nanoseconds, milliseconds, seconds)

	if measurements.count(None) != 2:
		raise ValueError(
			"Either `nanoseconds`, `milliseconds`, or `seconds` should be set; all three cannot be set, at least one must be set"
		)
	
	NANOSECONDS = 0

	if seconds: NANOSECONDS = seconds*1_000_000_000
	elif milliseconds: NANOSECONDS = milliseconds*1000
	else: NANOSECONDS = nanoseconds
	
	def wrapper(func: FunctionType):
		def inner(*args, **kwargs):
			if suppress_output:
				with contextlib.redirect_stdout(unittest.mock.Mock()): 
					start = time.perf_counter_ns()
					res = func(*args, **kwargs)
					length = time.perf_counter_ns()-start
			else:
				start = time.perf_counter_ns()
				res = func(*args, **kwargs)
				length = time.perf_counter_ns()-start

			if length > NANOSECONDS:
				if verbose:
					frame = inspect.currentframe().f_back
					line = traceback.format_list(traceback.extract_stack(limit=2))[0].split('\n')[1].strip()
					
					msg = f"perftest:\n\t{repr(line)}\n\t\ton line {inspect.getlineno(frame)}\n\t\tin file {inspect.getfile(frame)}\n\ttook more than the expected time!\n\t\treal: {length}ns\n\t\texpected: {NANOSECONDS}ns"

					if warn: warnings.warn(msg, RuntimeWarning, stacklevel=2)
					if throw: raise RuntimeError(msg)

					return res
				
				if warn:
					warnings.warn(
						f"perftest: {func.__name__} took more than the expected time!",
						RuntimeWarning, stacklevel=2
					)

				if throw:
					raise RuntimeError(
						f"perftest: {func.__name__} took more than the expected time!"
					)

			return res

		return inner
	
	return wrapper

def timeout(nanoseconds: int=None, milliseconds: int=None, seconds: int=None, *, verbose=False, suppress_output=False):	
	"""Timeout a function after a certain amount of time. If the function completed, its return value is returned, otherwise, `None` is returned, but the function may continue executing in the background until it completes OR the interpreter exits."""
	
	measurements = (nanoseconds, milliseconds, seconds)

	if measurements.count(None) != 2:
		raise ValueError(
			"Either `nanoseconds`, `milliseconds`, or `seconds` should be set; all three cannot be set, at least one must be set"
		)
	
	SECONDS = 0

	if seconds: SECONDS = seconds
	elif milliseconds: SECONDS = milliseconds/1000
	else: SECONDS = nanoseconds/1_000_000_000
	
	def wrapper(func: FunctionType):
		def inner(*args, **kwargs):
			retval = []
			###### fix multiprocessing - doesn't allow local vars to be used

			# thread = multiprocessing.Process(target=lambda: retval.append(func()), args=args, kwargs=kwargs)
			# thread.daemon = True
			# thread.start()

			# thread.join(SECONDS)

			# if thread.is_alive():
			# 	thread.kill()
			# 	return None

			thread = threading.Thread(target=lambda *args, **kwargs: retval.append(func(*args, **kwargs)), args=args, kwargs=kwargs)
			thread.daemon = True
			thread.start()

			thread.join(SECONDS)

			if thread.is_alive(): return None

			return retval[0]

		return inner
	
	return wrapper