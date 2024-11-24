import unittest
import json
from app import app


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_total_spent_valid_user(self):
        # Test a valid user_id
        response = self.app.get('/total_spent/791')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('user_id', data)
        self.assertIn('total_spent', data)

    def test_total_spent_invalid_user(self):
        # Test an invalid user_id
        response = self.app.get('/total_spent/9999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_average_spending(self):
        # Test average spending endpoint
        response = self.app.get('/average_spending_by_age')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        expected_keys = ['18-24', '25-30', '31-36', '37-47', '>48']
        for key in expected_keys:
            self.assertIn(key, data)

    def test_high_spending_user_get(self):
        # Test retrieving high spending users
        response = self.app.get('/write_high_spending_user')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_high_spending_user_post(self):
        # Test adding a high spending user
        payload = {'user_id': 7, 'total_spending': 500.0}
        response = self.app.post(
            '/write_high_spending_user',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'User data inserted successfully')

    def test_high_spending_user_invalid_method(self):
        # Test invalid HTTP method
        response = self.app.put('/write_high_spending_user')
        self.assertEqual(response.status_code, 405)
        data = json.loads(response.data)  # Decode and parse the JSON response
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid HTTP method; please use GET or POST')


if __name__ == '__main__':
    unittest.main()
