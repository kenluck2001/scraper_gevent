import unittest

import sys
import os
sys.path.append(os.path.abspath('..'))


from HTTPClass import HTTPClass


class DumyClass:
    pass


class TestAPP(unittest.TestCase):
    """
      The class inherits from unittest
    """

    def setUp(self):
        """
            This method is called before each test
        """
        self.httpObj = HTTPClass()

    def tearDown(self):
        """
            This method is called after each test
        """
        pass

    def test_http_response_class(self):
        with self.assertRaises(Exception) as context:
            self.httpObj.getResponseStatus(DumyClass)

    def test_http_response_content_exception_when_url_and_interval_is_empty(self):
        with self.assertRaises(Exception) as context:
            self.httpObj.getContent(url="", interval="")

    def test_http_response_content_exception_when_interval_is_empty(self):
        with self.assertRaises(Exception) as context:
            self.httpObj.getContent(url="http://www.google.com", interval="")

    def test_http_response_content_exception_when_url_is_empty(self):
        with self.assertRaises(Exception) as context:
            self.httpObj.getContent(url="", interval=20)


if __name__ == "__main__":
    unittest.main()


"""

Method 	Checks that 	New in
assertEqual(a, b) 	a == b 	 
assertNotEqual(a, b) 	a != b 	 
assertTrue(x) 	bool(x) is True 	 
assertFalse(x) 	bool(x) is False 	 
assertIs(a, b) 	a is b 	2.7
assertIsNot(a, b) 	a is not b 	2.7
assertIsNone(x) 	x is None 	2.7
assertIsNotNone(x) 	x is not None 	2.7
assertIn(a, b) 	a in b 	2.7
assertNotIn(a, b) 	a not in b 	2.7
assertIsInstance(a, b) 	isinstance(a, b) 	2.7
assertNotIsInstance(a, b) 	not isinstance(a, b) 	2.7

"""
