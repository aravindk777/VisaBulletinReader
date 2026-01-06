"""
Unit tests for testing the routes of the Visa Bulletin Reader web application.
"""

import unittest
from server import app

class TestServer(unittest.TestCase):
    """
    Unit tests for testing the routes of the Visa Bulletin Reader web application.
    """
    def setUp(self):
        """
        Set up the test client for the Flask application.
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_about_route(self):
        """
        Test the '/about' route of the Visa Bulletin Reader web application.
        """
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About Visa Bulletin Reader', response.data)

    def test_references_route(self):
        """
        Test the '/references' route of the Visa Bulletin Reader web application.
        """
        response = self.app.get('/references')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'References', response.data)

if __name__ == '__main__':
    unittest.main()
