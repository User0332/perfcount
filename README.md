# PerfTest/PerfCount - a Python library used for performance testing

Install it with `pip install perftest`.

There are multiple decorators included for testing in the library, including `perftest.perf`, `perftest.perf_ns`, `perftest.shouldtake`, and `perftest.timeout`. The `perftest.time_this_program` module can be imported to time the program from the time of importing the `perftest.time_this_program` module to interpreter exit.

The command `perftest` can be used to measure execution time of a command. Ex. `perftest echo hello`.