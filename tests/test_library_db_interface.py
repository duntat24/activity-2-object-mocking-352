import unittest
from unittest.mock import Mock

from library.library_db_interface import Library_DB

class LibraryDBTest(unittest.TestCase):

    def setUp(self): 
        # Initializes a fresh db for each test
        self.test_library_db = Library_DB()

    def tearDown(self):
        # We need to close the db after each run 
        self.test_library_db.db.close()
    
    def test_get_patron_count_empty(self):
        # Since we haven't added any data to the db, it should start as empty
        expected_patron_count = 0
        actual_patron_count = self.test_library_db.get_patron_count()
        self.assertEqual(expected_patron_count, actual_patron_count)
