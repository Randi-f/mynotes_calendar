import unittest
from unittest.mock import patch, MagicMock
from flask import json
from app import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.get_db_connection')
    def test_get_events(self, mock_get_db_connection):
        # Mocking database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mocking the cursor's fetchall method to return test data
        mock_cursor.fetchall.return_value = [
            (1, 'testuser', '2024-03-10', '2024-03-11', 'Test Event')
        ]
        
        response = self.app.get('/get_events?username=testuser')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Test Event')
        
        mock_cursor.execute.assert_called_once_with("SELECT * FROM calendar WHERE userid = %s", ('testuser',))

    @patch('app.get_db_connection')
    def test_add_event(self, mock_get_db_connection):
        # Mocking database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mocking the cursor's fetchone method to return test data for the event id
        mock_cursor.fetchone.return_value = [1]
        
        # Test event data
        event_data = {
            "username": "testuser",
            "start": "2024-03-10",
            "end": "2024-03-11",
            "title": "Test Event"
        }
        
        response = self.app.post('/add_events', data=json.dumps(event_data), content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Event added successfully')
        
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
