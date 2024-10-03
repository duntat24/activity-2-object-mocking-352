import unittest
from unittest.mock import MagicMock
from unittest.mock import Mock

from library.library_db_interface import Library_DB
from library.patron import *
from tinydb import Query

class LibraryDBTest(unittest.TestCase):

    def setUp(self): 
        # Initializes a fresh db for each test
        self.test_library_db = Library_DB()
        self.test_library_db.db.close() # We need to close the db since its been opened
        self.test_library_db.db = Mock() # Replacing the db with a mock object that we can control

    def test_close_db(self):
        # Tests that the db's close method is invoked when we attempt to close the db through the interface
        self.test_library_db.close_db()
        self.test_library_db.db.close.assert_called()

    def test_get_patron_count_empty(self):
        # Tests getting the patron count when the db is empty
        expected_patron_count = 0
        self.test_library_db.db.all = MagicMock(return_value = []) # forcing the db to return an empty list
        actual_patron_count = self.test_library_db.get_patron_count()
        self.assertEqual(expected_patron_count, actual_patron_count)

    def test_get_patron_count_not_empty(self):
        # Tests getting the patron count when the db is not empty
        expected_patron_count = 1
        self.test_library_db.db.all = MagicMock(return_value = [{"fname": "First", "lname": "Last", "age": "23", "memberID": "8675309"}]) # forcing the db to return one patron
        actual_patron_count = self.test_library_db.get_patron_count()
        self.assertEqual(expected_patron_count, actual_patron_count)

    def test_get_all_patrons_empty(self):
        # Tests getting all the patrons in the db when the db is empty
        self.test_library_db.db.all = MagicMock(return_value = []) # forcing the db to return an empty list
        patron_list = self.test_library_db.get_all_patrons()
        self.assertEqual(0, len(patron_list))

    def test_insert_none_patron(self):
        # Tests attempting to add a patron of value None should return None 
        add_result = self.test_library_db.insert_patron(None)
        self.assertEqual(None, add_result)

    def test_insert_patron_exists(self):
        # Tests attempting to add a patron that already exists in the db, should return None
        patron = Patron("Hello", "Itsme", 22, 8675309)
        self.test_library_db.db.search = MagicMock(return_value = [{"fname": "First", "lname": "Last", "age": "23", "memberID": "8675309"}]) # Forcing a result to be returned when attempting to retrieve from the library db
        add_result = self.test_library_db.insert_patron(patron)
        self.assertEqual(None, add_result)

    def test_insert_patron_not_exists(self):
        # Tests attempting to add a patron that doesn't exist in the DB, should return an ID
        patron = Patron("Tommy", "T", 65, 8675309)
        result_id = 12345
        self.test_library_db.db.insert = MagicMock(return_value = result_id) # forcing a specific ID to be returned when atttempting to insert
        self.test_library_db.db.search = MagicMock(return_value = None) # forcing no result to be found when searching the db
        add_result = self.test_library_db.insert_patron(patron)
        self.assertEqual(result_id, add_result)

    def test_update_patron_none(self):
        # Tests attempting to update a patron with a value of None, should return None
        update_result = self.test_library_db.update_patron(None)
        self.assertEqual(None, update_result)

    def test_update_patron_valid(self):
        # Tests updating a validly constructed patron
        patron = Patron("Tommy", "T", 65, 8675309)
        patron_dict = {"fname": "Tommy", "lname": "T", "age": 65, "memberID": 8675309, "borrowed_books": []}
        query = Query()
        self.test_library_db.update_patron(patron)
        self.test_library_db.db.update.assert_called_with(patron_dict, query.memberID == patron.get_memberID())

    def test_retrieve_patron_doesnt_exist(self):
        # Testing the return of retrieving if the patron is not found in the db
        self.test_library_db.db.search = MagicMock(return_value = None) # forcing the db to indicate that the patron wasn't found
        fetch_result = self.test_library_db.retrieve_patron(12345) # The passed id shouldn't matter
        self.assertEqual(None, fetch_result)

    def test_retrieve_patron_exists(self):
        # Testing the return of retrieving a patron if a patron is returned by the db
        self.test_library_db.db.search = MagicMock(return_value = [{"fname": "First", "lname": "Last", "age": "23", "memberID": "8675309"}]) # Forcing a result to be returned when attempting to retrieve from the library db
        expected_result = Patron("First", "Last", "22", "8675309")
        fetch_result = self.test_library_db.retrieve_patron(12345) # The passed id shouldn't matter
        self.assertEqual(expected_result.get_memberID(), fetch_result.get_memberID()) # memberIDs are unique, so if they are the same then the objects are the same

    def test_convert_patron_to_db_format(self):
        # Testing converting a patron to the format expected by the db
        test_patron = Patron("First", "Last", "25", "12345678")
        expected_db_format = {"fname": "First", "lname": "Last", "age": "25", "memberID": "12345678", "borrowed_books": []}
        result_db_format = self.test_library_db.convert_patron_to_db_format(test_patron)
        self.assertEqual(expected_db_format, result_db_format)