from typing import Dict, Sequence
from collections import Counter

from schedule.PowerSchedule import PowerSchedule
from utils.Seed import Seed


class PathPowerSchedule(PowerSchedule):

    def __init__(self) -> None:
        super().__init__()
        # TODO

    def assign_energy(self, population: Sequence[Seed]) -> None:
        """Assign exponential energy inversely proportional to path frequency"""
        # TODO
        # 统计每条路径的频率
        path_counts = Counter(tuple(seed.coverage) for seed in population)
        
        # 计算总路径数
        total_paths = sum(path_counts.values())

        # 根据路径频率的倒数分配能量
        for seed in population:
            seed.energy = 1 / path_counts[tuple(seed.coverage)] / total_paths

class CoveragePowerSchedule(PowerSchedule):

    def __init__(self) -> None:
        super().__init__()

    def assign_energy(self, population: Sequence[Seed]) -> None:
        """Assign exponential energy inversely proportional to path frequency"""
        total_coverage = set.union(*(seed.coverage for seed in population))
        total_locations = len(total_coverage)

        for seed in population:
            seed.energy = len(seed.coverage) / total_locations
