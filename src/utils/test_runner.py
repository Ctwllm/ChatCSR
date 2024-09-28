import subprocess
import os


class TestRunner:

    def __init__(self, test_file_path, test_class_name, test_method_name):
        self.test_file_path = test_file_path
        self.test_class_name = test_class_name
        self.test_method_name = test_method_name