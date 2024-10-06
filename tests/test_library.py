import unittest
from library import library

from unittest.mock import Mock
import json

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.lib = library.Library()
        with open('tests_data/books.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('tests_data/import_json.txt', 'r') as f2:
            self.json_import = json.loads(f2.read())

    ############################################################################
    ################################ API METHODS ###############################
    ############################################################################

    # Test is_ebook

    def test_is_ebook_true(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.is_ebook('Name of the Wind'))

    def test_is_ebook_true_non_first(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.is_ebook('Seymour: an Introduction'))

    def test_is_ebook_true_wrong_capitalization(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.is_ebook('wise mans fear'))

    def test_is_ebook_false(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertFalse(self.lib.is_ebook('Mein Kampf'))



    # Test get_ebooks_count

    def test_get_ebooks_count_real(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.get_ebooks_count('Name of the Wind') > 0)

    def test_get_ebooks_count_fake(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_ebooks_count('Mein Kampf'), 0)



    # Test is_book_by_author

    def test_is_book_by_author_real_real(self):
        self.lib.api.get_ebooks = Mock(return_value=self.json_import)
        self.assertTrue(self.lib.is_book_by_author('Thoughtful Machine Learning with Python', 'Matthew Kirk'))
        
    def test_is_book_by_author_real_fake(self):
        self.lib.api.get_ebooks = Mock(return_value=self.json_import)
        self.assertFalse(self.lib.is_book_by_author('Thoughtful Machine Learning with Python', 'Matty Jean Lu Picard'))
        
    def test_is_book_by_author_fake_real(self):
        self.lib.api.get_ebooks = Mock(return_value=self.json_import)
        self.assertFalse(self.lib.is_book_by_author('Thoughtless Machine Learning with Mamba', 'Matthew Kirk'))
        
    def test_is_book_by_author_fake_fake(self):
        self.lib.api.get_ebooks = Mock(return_value=self.json_import)
        self.assertFalse(self.lib.is_book_by_author('Thoughtless Machine Learning with Mamba', 'Matty Jean Lu Picard'))

    def test_is_book_by_author_real_real_multiple_of_title(self):
        self.lib.api.get_ebooks = Mock(return_value=self.json_import)
        self.assertTrue(self.lib.is_book_by_author('Python Programming', 'Bill Norton'))

    def test_is_book_by_author_multiple_of_title_other_author(self):
        self.lib.api.get_ebooks = Mock(return_value=self.json_import)
        self.assertTrue(self.lib.is_book_by_author('Python Programming', 'tony f. charles'))
        
    def test_is_book_by_author_real_fake_multiple_of_title(self):
        self.lib.api.get_ebooks = Mock(return_value=self.json_import)
        self.assertFalse(self.lib.is_book_by_author('Python Programming', 'Billy Nortaniel'))
        
    def test_is_book_by_author_fake_real_multiple_of_title(self):
        self.lib.api.get_ebooks = Mock(return_value=self.json_import)
        self.assertFalse(self.lib.is_book_by_author('Mamba Programming', 'Bill Norton'))
        
    def test_is_book_by_author_fake_fake_multiple_of_title(self):
        self.lib.api.get_ebooks = Mock(return_value=self.json_import)
        self.assertFalse(self.lib.is_book_by_author('Mamba Programming', 'Billy Nortaniel'))



    # Test get_languages_for_book

    def test_get_languages_for_book_real(self):
        self.lib.api.get_ebooks = Mock(return_value=self.json_import)
        print(self.lib.is_book_by_author('Python Programming'))
        # I don't think this one works



    ############################################################################
    ################################# DB METHODS ###############################
    ############################################################################


if __name__ == '__main__':
    unittest.main()