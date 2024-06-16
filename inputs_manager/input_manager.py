# inputs_manager/input_manager.py

import os
import pickle

class InputManager:
    def __init__(self, storage_dir):
        self.storage_dir = storage_dir
        self.inputs = {}  # 输入文件的配置表

    def save_input(self, input_data):
        filename = os.path.join(self.storage_dir, f"input_{len(self.inputs)}.txt")
        with open(filename, "w") as f:
            f.write(input_data)
        self.inputs[filename] = {
            'timestamp': time.time(),
            'coverage': 0  # 初始覆盖率为0，可以根据需要扩展
        }
        return filename

    def load_input(self, filename):
        with open(filename, "r") as f:
            return f.read()

    def update_coverage(self, filename, coverage):
        if filename in self.inputs:
            self.inputs[filename]['coverage'] = coverage

    def get_all_inputs(self):
        return list(self.inputs.keys())

    def save_configuration_table(self, filename):
        with open(os.path.join(self.storage_dir, 'config_table_' + filename + '.pkl'), 'wb') as f:
            pickle.dump(self.inputs, f)

    def load_configuration_table(self, filename):
        config_file = os.path.join(self.storage_dir, 'config_table_' + filename + '.pkl')
        if os.path.exists(config_file):
            with open(config_file, 'rb') as f:
                self.inputs = pickle.load(f)
