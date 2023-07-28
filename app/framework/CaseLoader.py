import json


class CaseLoader:
    def __init__(self, case_file=None):
        self._case_file = case_file

    def _json_load(self):
        with open(self._case_file, "r") as json_file:
            data = json.load(json_file)
            return data

    @staticmethod
    def _assert_key(key):
        pass

    @staticmethod
    def _assert_value(value, key=None):
        pass

    def generator(self):
        return (case for case in self._case_file)
