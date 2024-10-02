import unittest
from library.library import Library
from unittest.mock import Mock

class TestLibrary(unittest.TestCase):

    # Test if two base libraries equal eachother
    def test_init(self):
        lib = Library()
        self.assertEqual(lib)

if __name__ == '__main__':
    unittest.main()