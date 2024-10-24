import unittest
from library import library

from unittest.mock import Mock
from unittest.mock import MagicMock, patch
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
        self.lib.api.get_ebooks = Mock(return_value=[self.books_data[0]]) # books_data[0] is the entry 'Name of the wind'
        self.assertTrue(self.lib.get_ebooks_count('Name of the Wind') > 0)

    def test_get_ebooks_count_fake(self):
         self.lib.api.get_ebooks = Mock(return_value=[])
         self.assertFalse(self.lib.get_ebooks_count('Fake Book'))



    # Test is_book_by_author

    def test_is_book_by_author_real_real(self):
        self.lib.api.books_by_author = Mock(return_value=['Thoughtful Machine Learning with Python'])
        self.assertTrue(self.lib.is_book_by_author('Matthew Kirk', 'Thoughtful Machine Learning with Python'))
   
    def test_is_book_by_author_real_fake(self):
        self.lib.api.books_by_author = Mock(return_value=[]) # This author has no books, so making a request for their books should return nothing
        self.assertFalse(self.lib.is_book_by_author('Matty Jean Lu Picard', 'Thoughtful Machine Learning with Python'))
        
    def test_is_book_by_author_fake_real(self):
        self.lib.api.books_by_author = Mock(return_value=['Thoughtful Machine Learning with Python'])
        self.assertFalse(self.lib.is_book_by_author('Matthew Kirk', 'Thoughtless Machine Learning with Mamba'))
        
    def test_is_book_by_author_fake_fake(self):
        self.lib.api.books_by_author = Mock(return_value=[])
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

    def test_register_patron_none(self):
        patronFirst = "Miles"
        patronLast = "Tallia"
        patronAge = "20"
        patronID = "2004"

        self.lib.register_patron = MagicMock(return_value = 2004)
        id = self.lib.register_patron(patronFirst,patronLast,patronAge,patronID)

        Patron.assert_called_with(patronFirst,patronLast,patronAge,patronID)
        self.assertEqual(id, 2004)



    # Test is_patron_registered

    def test_is_patron_registered(self):
        self.lib.db.insert_patron = MagicMock(return_value = 2004)
        self.lib.register_patron("Miles", "Tallia", "20", "2004")
        patron = Patron("Miles", "Tallia", "20", "2004")
        self.lib.db.retrieve_patron = MagicMock(return_value = patron)
        self.assertTrue(self.lib.is_patron_registered(patron))

    # def test_is_patron_not_registered(self):
    #     self.lib.db.insert_patron = MagicMock(return_value = 211)
    #     patroon = Patron("Fake", "Guy", "4", "211")
    #     patron = Patron("Miles", "Tallia", "20", "2004")
    #     self.lib.db.retrieve_patron = MagicMock(return_value = patron)
    #     self.assertFalse(self.lib.is_patron_registered(patroon))

        

    # Test borrow_book

    def test_borrow_book(self):
        self.lib.db.insert_patron = MagicMock(return_value = 2004) # forcing a return of the added member's id
        self.lib.register_patron("Miles", "Tallia", "20", "2004")
        patron = Patron("Miles", "Tallia", "20", "2004")

        self.lib.db.update_patron = MagicMock(return_value = None) # The return for this method isn't relevant, we just want to prevent reliance on a DB call that may not be correct
        self.lib.borrow_book("Name of the Wind", patron)

        # Not sure what this is supposed to do, this is also mocked at the top of the method so a little strange to test a mocked return value
        self.lib.db.update_patron.assert_called_with(patron)

        

    # Test is_book_borrowed

    def test_is_book_borrowed(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)

        self.lib.db.insert_patron = MagicMock(return_value = 2004) # forcing return of added patron's ID to mimic correct addition
        self.lib.register_patron("Miles", "Tallia", "20", "2004")
        patron = Patron("Miles", "Tallia", "20", "2004")

        self.lib.db.update_patron = MagicMock(return_value = None) # The return for this method isn't relevant, we just want to prevent reliance on a DB call that may not be correct
        self.lib.borrow_book("Name of the Wind", patron)

        self.assertTrue(self.lib.is_book_borrowed("Name of the Wind", patron))

        

    # Test return_borrowed_book

    def test_return_borrowed_book(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)

        self.lib.db.insert_patron = MagicMock(return_value = 2004) # Forcing a return of 2004 to mimic correct insertion
        self.lib.register_patron("Miles", "Tallia", "20", "2004")
        patron = Patron("Miles", "Tallia", "20", "2004")

        self.lib.db.update_patron = MagicMock(return_value = None) # The return for this doesn't matter, just need to prevent reliance on db call
        self.lib.borrow_book("Name of the Wind", patron)

        self.lib.return_borrowed_book("Name of the Wind", patron)

        self.assertFalse(self.lib.is_book_borrowed("Name of the Wind", patron))
        


if __name__ == '__main__':
    unittest.main()