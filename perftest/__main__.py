import sys
import time
import subprocess

def main():
	cmd = sys.argv[1:]

	start = time.perf_counter_ns()

	subprocess.call(cmd)

	print(f"{' '.join(cmd)!r} took {time.perf_counter_ns()-start}ns")

if __name__ == "__main__":
	main()