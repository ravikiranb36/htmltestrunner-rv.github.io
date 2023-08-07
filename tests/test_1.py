import unittest


class TestCase1(unittest.TestCase):

    def test_upper(self):
        print("log")
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        print("log")
        self.assertTrue('FOO'.isupper())
        self.assertTrue('Foo'.isupper())

    def test_subtests(self):
        names = ["Ravikiran", "Viveka", "Mahalakshmi"]
        for i, name in enumerate(names, 1):
            if i % 2 == 0:
                name_to_compare = name
            else:
                name_to_compare = "Anamika"
            with self.subTest(f"sub test {i}"):
                self.assertEqual(name, name_to_compare)


if __name__ == '__main__':
    unittest.main()
