# inputs_manager/configuration_table.py

class ConfigurationTable:
    def __init__(self):
        self.config = {}

    def add_entry(self, filename, metadata):
        self.config[filename] = metadata

    def remove_entry(self, filename):
        if filename in self.config:
            del self.config[filename]

    def get_metadata(self, filename):
        return self.config.get(filename, {})

    def get_all_entries(self):
        return list(self.config.keys())
