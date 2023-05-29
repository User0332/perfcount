# PerfCount - a Python library used for performance testing

Install it with `pip install perfcount`.

There are multiple decorators included for testing in the library, including `perf.perf`, `perfcount.perf_ns`, `perfcount.shouldtake`, and `perfcount.timeout`. The `perfcount.time_this_program` module can be imported to time the program from the time of importing the `perfcount.time_this_program` module to interpreter exit.

The command `perftcount` can be used to measure execution time of a command. Ex. `perfcount python script.py`.