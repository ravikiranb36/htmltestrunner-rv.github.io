import unittest

class TestError(unittest.TestCase):
    """Testing error scenarios"""
    
    def test_runtime_error(self):
        """This test raises a ZeroDivisionError"""
        print("Intentional error: dividing by zero...")
        return 1 / 0

    def test_value_error(self):
        """This test raises a ValueError"""
        print("Intentional error: invalid value...")
        int("abc")
