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

    # report translate tests
    def test_report_translation_success(self):
        """Test report translation with valid input"""
        sample_input = {
            "language": "EN",
            "report": "This is a sample report."
        }
        response = self.client.post('/report/translate', json=sample_input)
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertIn('reportPL', response_data)
        self.assertIn('reportEN', response_data)
        self.assertIn('reportRU', response_data)
        self.assertIn('reportUA', response_data)

    def test_report_translation_invalid_json(self):
        """Test report translation with invalid JSON input"""
        invalid_input = {
            "invalidField": "Invalid data"
        }
        response = self.client.post('/report/translate', json=invalid_input)
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertIn('error', response_data)
        self.assertTrue(response_data['error'].startswith('Missing key'))

    # organisation translate tests
    def test_organisation_translation_success(self):
        """Test organisation translation with valid input"""
        sample_input = {
            "language": "EN",
            "description": "This is a sample organisation description."
        }
        response = self.client.post('/organisation/translate', json=sample_input)
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertIn('descriptionPL', response_data)
        self.assertIn('descriptionEN', response_data)
        self.assertIn('descriptionRU', response_data)
        self.assertIn('descriptionUA', response_data)

    def test_organisation_translation_invalid_json(self):
        """Test organisation translation with invalid JSON input"""
        invalid_input = {
            "invalidField": "Invalid data"
        }
        response = self.client.post('/organisation/translate', json=invalid_input)
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertIn('error', response_data)
        self.assertTrue(response_data['error'].startswith('Missing key'))

    # faq translate tests
    def test_faq_translation_success(self):
        """Test FAQ translation with valid input"""
        sample_input = {
            "language": "EN",
            "question": "What is this?",
            "answer": "This is a FAQ answer."
        }
        response = self.client.post('/faq/translate', json=sample_input)
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertIn('questionPL', response_data)
        self.assertIn('questionEN', response_data)
        self.assertIn('questionRU', response_data)
        self.assertIn('questionUA', response_data)
        self.assertIn('answerPL', response_data)
        self.assertIn('answerEN', response_data)
        self.assertIn('answerRU', response_data)
        self.assertIn('answerUA', response_data)

    def test_faq_translation_invalid_json(self):
        """Test FAQ translation with invalid JSON input"""
        invalid_input = {
            "invalidField": "Invalid data"
        }
        response = self.client.post('/faq/translate', json=invalid_input)
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertIn('error', response_data)
        self.assertTrue(response_data['error'].startswith('Missing key'))


if __name__ == '__main__':
    unittest.main()
