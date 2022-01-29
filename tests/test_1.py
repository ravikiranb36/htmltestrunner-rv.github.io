import unittest


class TestCase1(unittest.TestCase):

    def test_upper(self):
        print("log")
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        print("log")
        self.assertTrue('FOO'.isupper())
        self.assertTrue('Foo'.isupper())


if __name__ == '__main__':
    unittest.main()
