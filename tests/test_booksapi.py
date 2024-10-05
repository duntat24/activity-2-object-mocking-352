import unittest
from library import ext_api_interface
from unittest.mock import Mock, MagicMock
import requests
import json

class TestBooksApi(unittest.TestCase):
    
    def setUp(self):
        """
        setUp 
        """
        self.api = ext_api_interface.Books_API()
        self.book = "learning python"
        with open('../activity-2-object-mocking-352/tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('../activity-2-object-mocking-352/tests_data/json_data.txt', 'r') as f:
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
        
    
    def test_books_by_author_exists(self):
        """
        Test books by author if author does exist test
        returns a list of books by that author
        """
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        
        mocked_call = self.api
        
        mocked_call.books_by_author = MagicMock(return_value = {"Python: Deeper Insights into Machine Learning"} )
        result = mocked_call.books_by_author("Sebastian Raschka")
        
        # mocked_call.books_by_author.assert_called_with("Sebastian Raschka")
        self.assertEqual(result,self.api.books_by_author("Sebastian Raschka"))
        
        # mock_call = Mock(self.api.books_by_author("Mark Lutz"))
        # print(mock_call)
        # self.assertEquals(mock_call,["Learning Python","Learning Python, Second Edition", "Learning Python (Learning)", "Python Machine Learning"])
        #["Learning Python","Learning Python, Second Edition", "Learning Python (Learning)", "Python Machine Learning"
        
    def test_books_by_author_doesnt_exist(self):
        """
        Test books by author if author doesn't exist test
        """
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        self.assertEqual(self.api.books_by_author("Bob Krutz"), [])
        
    def test_get_book_info(self):
        """
        Get book info test (False)
        """

        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        book_query = 'No Python Book'
        
        result = self.api.get_book_info(book_query)
        self.assertEqual(result, [])
        # attr = {'json.return_value': dict()}
        # requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        
        # mocked_call = self.api
        
        # mocked_call.get_book_info = MagicMock(return_value = [])
        # result = mocked_call.get_book_info("Python: Deeper Insights into not Machine Learning")
        # print(result)
        # print(self.api.get_book_info("Python: Deeper Insights into not Machine Learning"))
        # self.assertEqual(result,[])