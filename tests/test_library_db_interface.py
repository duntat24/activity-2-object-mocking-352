import unittest
from unittest.mock import MagicMock

from library.library_db_interface import Library_DB
from library.patron import *

class LibraryDBTest(unittest.TestCase):

    def setUp(self): 
        # Initializes a fresh db for each test
        self.test_library_db = Library_DB()

    def tearDown(self):
        # We need to close the db after each run or we get warnings
        self.test_library_db.db.close()
    
    def test_get_patron_count_empty(self):
        # Forcing the return value from the db to be an empty list
        expected_patron_count = 0
        self.test_library_db.db.all = MagicMock(return_value = []) # forcing the db to return an empty list
        actual_patron_count = self.test_library_db.get_patron_count()
        self.assertEqual(expected_patron_count, actual_patron_count)

    def test_get_patron_count_not_empty(self):
        # Forcing the return value from the db to contain a patron
        expected_patron_count = 1
        self.test_library_db.db.all = MagicMock(return_value = [{"fname": "First", "lname": "Last", "age": "23", "memberID": "8675309"}]) # forcing the db to return one patron
        actual_patron_count = self.test_library_db.get_patron_count()
        self.assertEqual(expected_patron_count, actual_patron_count)

    def test_get_all_patrons_empty(self):
        # Since we haven't added any data to the db, getting all patrons should return an empty list
        self.test_library_db.db.all = MagicMock(return_value = []) # forcing the db to return an empty list
        patron_list = self.test_library_db.get_all_patrons()
        self.assertEqual(0, len(patron_list))

    def test_insert_none_patron(self):
        # Attempting to add a patron of value None should return None 
        add_result = self.test_library_db.insert_patron(None)
        self.assertEqual(None, add_result)

    def test_insert_patron_exists(self):
        # Attempting to add a patron that already exists in the db, should return None
        patron = Patron("Hello", "Itsme", 22, 8675309)
        self.test_library_db.db.search = MagicMock(return_value = [{"fname": "First", "lname": "Last", "age": "23", "memberID": "8675309"}]) # Forcing a result to be returned when attempting to retrieve from the library db
        add_result = self.test_library_db.insert_patron(patron)
        self.assertEqual(None, add_result)

    def test_insert_patron_not_exists(self):
        # Attempting to add a patron that doesn't exist in the DB, should return an ID
        patron = Patron("Tommy", "T", 65, 8675309)
        result_id = 12345
        self.test_library_db.db.insert = MagicMock(return_value = result_id) # forcing a specific ID to be returned when atttempting to insert
        self.test_library_db.db.search = MagicMock(return_value = None) # forcing no result to be found when searching the db
        add_result = self.test_library_db.insert_patron(patron)
        self.assertEqual(result_id, add_result)
        

