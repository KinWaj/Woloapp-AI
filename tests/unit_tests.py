"""Module for unit tests"""
import unittest
from app import app


class WoloAppTestCase(unittest.TestCase):
    """Testing class for whole application"""
    def setUp(self):
        """Set up the test environment"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Tear down the test environment"""
        self.app_context.pop()

    # event create test
    def test_event_creation_success(self):
        """Test event creation with valid input"""
        sample_input = {
            "language": "EN",
            "name": "Sample Event",
            "description": "This is a sample event.",
            "shiftDirections": ["Sample directions", ""]
        }
        response = self.client.post('/event-create', json=sample_input)
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertIn('namePL', response_data)
        self.assertIn('descriptionPL', response_data)
        self.assertIn('shiftTranslations', response_data)
        self.assertIsInstance(response_data['shiftTranslations'], list)
        self.assertIn('addressDescriptionPL', response_data['shiftTranslations'][0])

    def test_event_creation_invalid_json(self):
        """Test event creation with invalid JSON input"""
        invalid_input = {
            "invalidField": "Invalid data"
        }
        response = self.client.post('/event-create', json=invalid_input)
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertIn('error', response_data)
        self.assertTrue(response_data['error'].startswith('Missing key'))

    # report tests
    # organisation tests
    # faq tests


if __name__ == '__main__':
    unittest.main()
