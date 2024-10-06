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
        returns a list of books by that author
        """
        
        attr = {'json.return_value':  {"docs": [{"author_name": ["Sebastian Raschka"]}]}}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        self.assertEqual(self.api.books_by_author("Sebastian Raschka"),attr)
        
        
        # attr = {'json.return_value': [{"author_name": ["Sebastian Raschka"]}]}
        #attr = {"docs": {"author_name": "Sebastian Raschka"}}
        # {'json.return_value': {"author_name": 'Sebastian Raschka'}.json()}
        
        # self.api.make_request = MagicMock(return_value =self.json_data)
        
        # self.api.make_request("http://openlibrary.org/search.json")
        
        # books = self.api.books_by_author('Sebastian Raschka')
        
        # expected_books = ['Learning python']
        
        # print(self.api.make_request)
        # print(self.api.books_by_author("Sebastian Raschka"))
        # self.assertEqual(books, expected_books)
        
        # attr = {'json.return_value': dict()}
        # requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        

        
        # mock = Mock()
        # mock.self.api.books_by_author("Sebastian Raschka")
        
        # result = self.api.books_by_author("Sebastian Raschka")
        
        # mocked_call.books_by_author.assert_called_with("Sebastian Raschka")
        # self.assertEqual(self.api.books_by_author("Sebastian Raschka"), [])
        
        # mock_call = Mock(self.api.books_by_author("Mark Lutz"))
        # print(mock_call)
        # self.assertEquals(mock_call,["Learning Python","Learning Python, Second Edition", "Learning Python (Learning)", "Python Machine Learning"])
        #["Learning Python","Learning Python, Second Edition", "Learning Python (Learning)", "Python Machine Learning"
        
    def test_books_by_author_false(self):
        """
        Test books by author if author doesn't exist test
        """
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        self.assertEqual(self.api.books_by_author("Bob Krutz"), [])
        
    def test_get_book_info_doesnt_exist(self):
        """
        Get book info test (False)
        """

        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        book_query = 'No Python Book'
        
        result = self.api.get_book_info(book_query)
        self.assertEqual(result, [])
        
    
    def test_get_book_info_true(self):
        """
        Get book info test (True)
        """
        attr = {'docs': [{'title': 'Learning Python', 'publisher': 'O\'Reilly Media', 'publish_year': [1999], 'language': ['eng']}]}

        
        self.api.make_request = MagicMock(return_value=attr)

        books_info = self.api.get_book_info('Learning Python')
        
        expected_url = 'http://openlibrary.org/search.json?q=Learning Python'
        self.api.make_request.assert_called_with(expected_url)

        expected_books_info = [{'title': 'Learning Python', 'publisher': 'O\'Reilly Media', 'publish_year': [1999], 'language': ['eng']}]

        self.assertEqual(books_info, expected_books_info)
        
    def test_get_ebooks(self):
        """
        Get ebooks test (False)
        """

        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        book_query = 'No Python Book'
        
        result = self.api.get_ebooks(book_query)
        self.assertEqual(result, [])