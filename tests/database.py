import unittest
from unittest.mock import patch 
from unittest import mock
import time
 # Patching for mocking database interactions
# Replace with the actual path to your DBConnection class
from sick_src.database import DBConnection


class TestDBConnection(unittest.TestCase):

    # Patch the sqlite3.connect method to avoid actual database interaction
    @patch('sqlite3.connect')
    


if __name__ == '__main__':
    unittest.main()
