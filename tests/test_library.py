import unittest
from library import library

from unittest.mock import Mock
from unittest.mock import MagicMock
import json

from library.patron import Patron

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.lib = library.Library()
        with open('tests/library_test_data/books.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('tests/library_test_data/import_json.txt', 'r') as f2:
            self.json_import = json.loads(f2.read())
        
    def tearDown(self):
        self.lib.db.close_db() # Need to close the DB to prevent a warning

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
        self.assertFalse(self.lib.is_ebook('Fake Book'))



    # Test get_ebooks_count

    def test_get_ebooks_count_real(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.get_ebooks_count('Name of the Wind') > 0)

    # def test_get_ebooks_count_fake(self):
    #     self.lib.api.get_ebooks = Mock(return_value=self.books_data)
    #     self.assertFalse(self.lib.get_ebooks_count('Fake Book'))



    # Test is_book_by_author

    def test_is_book_by_author_real_real(self):
        self.lib.api.make_request = Mock(return_value=self.json_import)
        self.assertTrue(self.lib.is_book_by_author('Matthew Kirk', 'Thoughtful Machine Learning with Python'))
   
    def test_is_book_by_author_real_fake(self):
        self.lib.api.get_ebooks = Mock(return_value=self.json_import)
        self.assertFalse(self.lib.is_book_by_author('Matty Jean Lu Picard', 'Thoughtful Machine Learning with Python'))
        
    def test_is_book_by_author_fake_real(self):
        self.lib.api.get_ebooks = Mock(return_value=self.json_import)
        self.assertFalse(self.lib.is_book_by_author('Matthew Kirk', 'Thoughtless Machine Learning with Mamba'))
        
    def test_is_book_by_author_fake_fake(self):
        self.lib.api.get_ebooks = Mock(return_value=self.json_import)
        self.assertFalse(self.lib.is_book_by_author('Matty Jean Lu Picard', 'Thoughtless Machine Learning with Mamba'))



    # Test get_languages_for_book

    def test_get_languages_for_book_real(self):
        self.lib.api.make_request = Mock(return_value=self.json_import)
        self.assertTrue(self.lib.get_languages_for_book('Python Programming').__contains__("eng"))



    ############################################################################
    ################################# DB METHODS ###############################
    ############################################################################

    # Test register_patron

    def test_register_patron(self):
        self.lib.register_patron = MagicMock(return_value = 2004)
        id = self.lib.register_patron("Miles", "Tallia", "20", "2004")
        self.assertEqual(id, 2004)



    # Test is_patron_registered

    def test_is_patron_registered(self):
        self.lib.register_patron("Miles", "Tallia", "20", "2004")
        patron = Patron("Miles", "Tallia", "20", "2004")
        self.assertTrue(self.lib.is_patron_registered(patron))

        

    # Test borrow_book

    def test_borrow_book(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)

        self.lib.register_patron("Miles", "Tallia", "20", "2004")
        patron = Patron("Miles", "Tallia", "20", "2004")

        self.lib.borrow_book("Name of the Wind", patron)

        self.assertTrue(self.lib.api.get_ebooks)

        

    # Test is_book_borrowed

    def test_is_book_borrowed(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)

        self.lib.register_patron("Miles", "Tallia", "20", "2004")
        patron = Patron("Miles", "Tallia", "20", "2004")

        self.lib.borrow_book("Name of the Wind", patron)

        self.assertTrue(self.lib.is_book_borrowed("Name of the Wind", patron))

        

    # Test return_borrowed_book

    def test_return_borrowed_book(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)

        self.lib.register_patron("Miles", "Tallia", "20", "2004")
        patron = Patron("Miles", "Tallia", "20", "2004")

        self.lib.borrow_book("Name of the Wind", patron)

        self.lib.return_borrowed_book("Name of the Wind", patron)

        self.assertFalse(self.lib.is_book_borrowed("Name of the Wind", patron))
        


if __name__ == '__main__':
    unittest.main()