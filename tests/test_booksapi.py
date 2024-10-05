import unittest
from library import ext_api_interface
from unittest.mock import Mock
import requests
import json

class TestBooksApi(unittest.TestCase):
    
    def setUp(self):
        """
        setUp 
        """
        self.api = ext_api_interface.Books_API()
        self.book = "learning python"
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('tests_data/json_data.txt', 'r') as f:
            self.json_data = json.loads(f.read())
    
    
    def test_make_request_true(self):
        """
        Make request true test
        """
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        self.assertEqual(self.api.make_request("http://openlibrary.org/search.json"), dict())

    
    def test_make_request_false(self):
        """
        Make request false test
        """
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 100,**attr) )
        self.assertEqual(self.api.make_request("http://openlibrary.org/fchjbnkm"), None)
    
    
    
    def test_make_request_connection_error(self):
        """
        Make request connection error test
        """
        ext_api_interface.requests.get = Mock(side_effect=requests.ConnectionError)
        url = "http://openlibrary.org/search.json"
        self.assertEqual(self.api.make_request(url), None)
    
    
    def test_is_book_available_false(self):
        """
        is Book available test (False)
        """
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        
        self.assertEqual(self.api.is_book_available(self.book), False)
        
    @Mock('ext_api_interface.is_book_available')
    def test_is_book_available_true(self):
        """
        is Book available test (True)
        """
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        self.assertEqual(self.api.is_book_available("Protected DAISY"), True)
        
    
    @Mock('ext_api_interface.books_by_author_exists')
    def test_books_by_author_exists(self):
        """
        Test books by author if author does exist test
        """
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        
        
        
        self.assertEquals(self.api.books_by_author("Mark Lutz"),["Learning Python","Learning Python, Second Edition", "Learning Python (Learning)", "Python Machine Learning"])
        #["Learning Python","Learning Python, Second Edition", "Learning Python (Learning)", "Python Machine Learning"
        
    def test_books_by_author_doesnt_exist(self):
        """
        Test books by author if author doesn't exist test
        """
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        self.assertEqual(self.api.books_by_author("Bob Krutz"), [])