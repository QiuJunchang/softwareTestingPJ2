import os
import time

from fuzzer.PathGreyBoxFuzzer import PathGreyBoxFuzzer
from runner.FunctionCoverageRunner import FunctionCoverageRunner
from schedule.PathPowerSchedule import PathPowerSchedule, CoveragePowerSchedule
from utils.ObjectUtils import dump_object, load_object

from samples.Samples import sample1, sample2, sample3, sample4

from inputs_manager.input_manager import InputManager

class Result:
    def __init__(self, coverage, crashes, start_time, end_time):
        self.covered_line = coverage
        self.crashes = crashes
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return f"Covered Lines: {self.covered_line}, Crashes Num: {self.crashes}, Start Time: {self.start_time}, End Time: {self.end_time}"

if __name__ == "__main__":
    storage_dir = "inputs_storage"  # 设定存储输入的文件夹路径
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)

    # 创建输入管理器实例
    input_manager = InputManager(storage_dir)
    input_manager.load_configuration_table("sample2")  # 加载配置表

    f_runner = FunctionCoverageRunner(sample2)
    seeds = load_object("corpus/corpus_2")

    grey_fuzzer = PathGreyBoxFuzzer(seeds=seeds, schedule=CoveragePowerSchedule(), is_print=True)
    start_time = time.time()
    grey_fuzzer.runs(f_runner, run_time=300)

    # 保存结果
    res = Result(grey_fuzzer.covered_line, set(grey_fuzzer.crash_map.values()), start_time, time.time())
    dump_object("_result" + os.sep + "Sample-2.pkl", res)

    # 保存配置表
    input_manager.save_configuration_table("sample2")

    # 输出结果
    print(load_object("_result" + os.sep + "Sample-2.pkl"))
