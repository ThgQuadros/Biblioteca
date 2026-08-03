import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app


class AppSmokeTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_livros_page(self):
        response = self.client.get('/livros')
        self.assertEqual(response.status_code, 200)

    def test_usuarios_page(self):
        response = self.client.get('/usuarios')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
