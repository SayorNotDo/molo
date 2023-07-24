class CaseLoader:
    def __init__(self):
        self.case_list = None

    @staticmethod
    def _assert_key(key):
        pass

    @staticmethod
    def _assert_value(value, key=None):
        pass

    def generator(self):
        return (case for case in self.case_list)
