import time
from typing import List, Tuple, Any

from fuzzer.GreyBoxFuzzer import GreyBoxFuzzer
from schedule.PathPowerSchedule import PathPowerSchedule
from runner.FunctionCoverageRunner import FunctionCoverageRunner


class PathGreyBoxFuzzer(GreyBoxFuzzer):
    """Count how often individual paths are exercised."""

    def __init__(self, seeds: List[str], schedule: PathPowerSchedule, is_print: bool):
        super().__init__(seeds, schedule, False)

        # TODO
        self.path_frequency = {}
        self.start_time = time.time()
        self.path_time = self.start_time
        self.last_crash_time = self.start_time
        self.total_exec = 0
        self.total_path = 0
        self.covered_line = set()
        self.crash_map = {}

        if is_print:
            print("""
┌───────────────────────┬───────────────────────┬───────────────────────┬───────────────────┬───────────────────┬────────────────┬───────────────────┐
│        Run Time       │     Last New Path     │    Last Uniq Crash    │    Total Execs    │    Total Paths    │  Uniq Crashes  │   Covered Lines   │
├───────────────────────┼───────────────────────┼───────────────────────┼───────────────────┼───────────────────┼────────────────┼───────────────────┤""")

    def print_stats(self):
        def format_seconds(seconds):
            hours = int(seconds) // 3600
            minutes = int(seconds % 3600) // 60
            remaining_seconds = int(seconds) % 60
            return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"

        template = """│{runtime}│{path_time}│{crash_time}│{total_exec}│{total_path}│{uniq_crash}│{covered_line}│
├───────────────────────┼───────────────────────┼───────────────────────┼───────────────────┼───────────────────┼────────────────┼───────────────────┤"""
        template = template.format(runtime=format_seconds(time.time() - self.start_time).center(23),
                                   path_time=format_seconds(time.time() - self.path_time).center(23),
                                   crash_time=format_seconds(self.last_crash_time - self.start_time).center(23),
                                   total_exec=str(self.total_execs).center(19),
                                   total_path=str(self.total_path).center(19),
                                   uniq_crash=str(len(set(self.crash_map.values()))).center(16),
                                   covered_line=str(len(self.covered_line)).center(19))
        print(template)

    def run(self, runner: FunctionCoverageRunner) -> Tuple[Any, str]:  # type: ignore
        """Inform scheduler about path frequency"""
        result, outcome = super().run(runner)

        # TODO
        path = hash(frozenset(runner.coverage()))
        self.total_execs += 1

        # Update path frequency and check for new paths
        if path not in self.path_frequency:
            self.path_frequency[path] = 0
            self.total_path += 1
            self.path_time = time.time()
        self.path_frequency[path] += 1

        # Update coverage information
        self.covered_line.update(runner.coverage())

        # Update crash information
        if outcome == "crash":
            self.crash_map[path] = result
            self.last_crash_time = time.time()

        return result, outcome
