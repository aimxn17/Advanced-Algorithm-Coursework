# Question 3 -> Concurrent Process (multi vs single thread)

import threading
import time
import math

#  FACTORIAL FUNCTION
def factorial(n: int) -> int:
    result = 1  # 1 operation
    for i in range(1, n + 1):
        result *= i  # 1 multiplication per iteration
    return result

#  MULTITHREADING EXPERIMENT
def run_multithreaded_round(targets: list[int]) -> int:
    #Spawn one thread per target, run all concurrently.
    results = {}
    lock = threading.Lock()

    # Track per-thread start/end times
    start_times = {}
    end_times = {}

    def thread_task(n: int) -> None:
        start_times[n] = time.perf_counter_ns()
        results[n] = factorial(n)
        end_times[n] = time.perf_counter_ns()

    # Create one thread per factorial target
    threads = [threading.Thread(target=thread_task, args=(n,)) for n in targets]

    # Start all threads as close together as possible
    for t in threads:
        t.start()
    for t in threads:     # Wait for all threads to finish
        t.join()

    # Apply formula: Elapsed = End of last-finishing thread – Start of first-starting thread
    first_start = min(start_times.values())
    last_end = max(end_times.values())
    return last_end - first_start


#  SINGLE-THREAD EXPERIMENT
def run_singlethread_round(targets: list[int]) -> int:
    """
    Run all factorials sequentially in the main thread.
    Returns total elapsed time in nanoseconds.
    """
    start = time.perf_counter_ns()
    for n in targets:
        factorial(n)
    end = time.perf_counter_ns()
    return end - start

#  DISPLAY HELPERS
DIVIDER = "=" * 68
SUB_DIVIDER = "-" * 68
ROUNDS = 10
TARGETS = [50, 100, 200]


def print_calculate(label: str, times_ns: list[int]) -> None:
    avg = sum(times_ns) / len(times_ns)
    print(f"  {SUB_DIVIDER}")
    print(f"  {'TOTAL':<8} {sum(times_ns):>18,} ns")
    print(f"  {'AVERAGE':<8} {avg:>18,.0f} ns")
    print(f"  {SUB_DIVIDER}")
    return avg


#  Main
def main() -> None:

    #Multithreaded rounds
    print("  1. MULTITHREADING - (3 threads, 1 each)")
    print(f"  {SUB_DIVIDER}")
    print(f"  {'Round':>7} {'Time Taken (ns)':>25}")
    print(f"  {SUB_DIVIDER}")

    mt_times = []
    for r in range(1, ROUNDS + 1):
        elapsed = run_multithreaded_round(TARGETS)
        mt_times.append(elapsed)
        print(f"    Round {r:>2}: {elapsed:>15,} ns")
    mt_avg = print_calculate("Multithreaded — Results Table", mt_times)


    # Single thread rounds
    print(f"\n{DIVIDER}")
    print("  2. SINGLE-THREAD ")
    print(f"  {SUB_DIVIDER}")
    print(f"  {'Round':>7} {'Time Taken (ns)':>25}")
    print(f"  {SUB_DIVIDER}")

    st_times = []
    for r in range(1, ROUNDS + 1):
        elapsed = run_singlethread_round(TARGETS)
        st_times.append(elapsed)
        print(f"    Round {r:>2}: {elapsed:>15,} ns")

    st_avg = print_calculate("Single-Thread — Results Table", st_times)


if __name__ == "__main__":
    main()
