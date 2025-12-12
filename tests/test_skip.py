import unittest


class TestSkipped(unittest.TestCase):

    def test_pass(self):
        self.assertEqual('foo'.upper(), 'FOO')

    @unittest.skip("Demonstrating skipping")
    def test_skip_decorator(self):
        self.fail("This should be skipped")

    def test_skip_method(self):
        self.skipTest("Skipping this test using skipTest method")

    @unittest.skipIf(True, "Skipping because condition is True")
    def test_skip_if(self):
        self.fail("This should be skipped")

    @unittest.skipUnless(False, "Skipping because condition is False")
    def test_skip_unless(self):
        self.fail("This should be skipped")


if __name__ == '__main__':
    unittest.main()
