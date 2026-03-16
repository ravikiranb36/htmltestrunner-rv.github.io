import unittest

class TestSubTest(unittest.TestCase):
    def test_subtests_success(self):
        """Test with successful subtests"""
        for i in range(0, 2):
            with self.subTest(i=i):
                self.assertEqual(i, i)

    def test_subtests_failure(self):
        """Test with failing subtests"""
        for i in range(0, 3):
            with self.subTest(i=i):
                if i == 1:
                    self.assertEqual(i, 0)
                else:
                    self.assertEqual(i, i)

if __name__ == '__main__':
    unittest.main()
