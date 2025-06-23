import unittest
import json
import sys
from unittest.mock import patch, MagicMock, Mock

mysql_mock = Mock()
mysql_mock.connector = Mock()
mysql_mock.connector.Error = Exception
mysql_mock.connector.connect = Mock()
sys.modules['mysql'] = mysql_mock
sys.modules['mysql.connector'] = mysql_mock.connector

from app import app

class TestEmployeeAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.sample_employee = {
            "id": "EMP001",
            "emp_name": "John Doe",
            "joining_date": "2024-01-15",
            "project_id": "PROJ001",
            "mobile_no": "1234567890",
            "email": "john@example.com",
            "role": "Employee"
        }

    @patch('app.execute_query')
    def test_add_employee_success(self, mock_execute):
        mock_execute.return_value = (True, "EMP001")
        
        response = self.app.post('/employees', 
                               data=json.dumps(self.sample_employee),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("Employee added successfully", data["message"])

    @patch('app.execute_query')
    def test_add_employee_duplicate_id(self, mock_execute):
        mock_execute.return_value = (False, "Duplicate entry 'EMP001' for key 'PRIMARY'")
        
        response = self.app.post('/employees',
                               data=json.dumps(self.sample_employee),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 409)

    def test_add_employee_missing_fields(self):
        incomplete_data = {"id": "EMP001", "emp_name": "John"}
        
        response = self.app.post('/employees',
                               data=json.dumps(incomplete_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_add_employee_invalid_role(self):
        invalid_employee = self.sample_employee.copy()
        invalid_employee["role"] = "InvalidRole"
        
        response = self.app.post('/employees',
                               data=json.dumps(invalid_employee),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_add_employee_invalid_date(self):
        invalid_employee = self.sample_employee.copy()
        invalid_employee["joining_date"] = "invalid-date"
        
        response = self.app.post('/employees',
                               data=json.dumps(invalid_employee),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_add_employee_no_json(self):
        response = self.app.post('/employees')
        # Flask returns 415 when no JSON is provided
        self.assertEqual(response.status_code, 415)

    # Test GET endpoints
    @patch('app.execute_query')
    def test_get_all_employees_success(self, mock_execute):
        mock_data = [
            {"id": "EMP001", "emp_name": "John", "joining_date": "2024-01-15"},
            {"id": "EMP002", "emp_name": "Jane", "joining_date": "2024-02-01"}
        ]
        mock_execute.return_value = (True, mock_data)
        
        response = self.app.get('/employees')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

    @patch('app.execute_query')
    def test_get_all_employees_failure(self, mock_execute):
        mock_execute.return_value = (False, "Database error")
        
        response = self.app.get('/employees')
        
        self.assertEqual(response.status_code, 500)

    @patch('app.execute_query')
    def test_get_employee_by_id_success(self, mock_execute):
        mock_data = {"id": "EMP001", "emp_name": "John", "joining_date": "2024-01-15"}
        mock_execute.return_value = (True, mock_data)
        
        response = self.app.get('/employees/EMP001')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["id"], "EMP001")

    @patch('app.execute_query')
    def test_get_employee_by_id_not_found(self, mock_execute):
        mock_execute.return_value = (True, None)
        
        response = self.app.get('/employees/INVALID')
        
        self.assertEqual(response.status_code, 404)

    @patch('app.execute_query')
    def test_get_employee_by_id_failure(self, mock_execute):
        mock_execute.return_value = (False, "Database error")
        
        response = self.app.get('/employees/EMP001')
        
        self.assertEqual(response.status_code, 500)

    # Test UPDATE endpoint
    @patch('app.execute_query')
    def test_update_employee_success(self, mock_execute):
        mock_execute.return_value = (True, None)
        update_data = {"emp_name": "Updated Name"}
        
        response = self.app.put('/employees/EMP001',
                              data=json.dumps(update_data),
                              content_type='application/json')
        
        self.assertEqual(response.status_code, 200)

    def test_update_employee_no_fields(self):
        response = self.app.put('/employees/EMP001',
                              data=json.dumps({}),
                              content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_update_employee_invalid_date(self):
        update_data = {"joining_date": "invalid-date"}
        
        response = self.app.put('/employees/EMP001',
                              data=json.dumps(update_data),
                              content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_update_employee_invalid_role(self):
        update_data = {"role": "InvalidRole"}
        
        response = self.app.put('/employees/EMP001',
                              data=json.dumps(update_data),
                              content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_update_employee_no_json(self):
        response = self.app.put('/employees/EMP001')
        self.assertEqual(response.status_code, 415)

    @patch('app.execute_query')
    def test_update_employee_database_error(self, mock_execute):
        mock_execute.return_value = (False, "Database error")
        update_data = {"emp_name": "Updated Name"}
        
        response = self.app.put('/employees/EMP001',
                              data=json.dumps(update_data),
                              content_type='application/json')
        
        self.assertEqual(response.status_code, 500)

    # Test DELETE endpoint
    @patch('app.execute_query')
    def test_delete_employee_success(self, mock_execute):
        mock_execute.return_value = (True, None)
        
        response = self.app.delete('/employees/EMP001')
        
        self.assertEqual(response.status_code, 200)

    @patch('app.execute_query')
    def test_delete_employee_database_error(self, mock_execute):
        mock_execute.return_value = (False, "Database error")
        
        response = self.app.delete('/employees/EMP001')
        
        self.assertEqual(response.status_code, 500)

    # Test database connection functions
    @patch('app.get_db_connection')
    def test_execute_query_connection_failure(self, mock_connection):
        from app import execute_query
        mock_connection.return_value = None
        
        success, result = execute_query("SELECT * FROM employees")
        
        self.assertFalse(success)
        self.assertIn("Database connection failed", result)

    @patch('app.mysql.connector.connect')
    def test_get_db_connection_success(self, mock_connect):
        from app import get_db_connection
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        connection = get_db_connection()
        
        self.assertEqual(connection, mock_conn)

    @patch('app.mysql.connector.connect')
    def test_get_db_connection_failure(self, mock_connect):
        from app import get_db_connection
        mock_connect.side_effect = Exception("Connection failed")
        
        connection = get_db_connection()
        
        self.assertIsNone(connection)

    def test_execute_query_with_mocked_db(self):
        from app import execute_query
        with patch('app.get_db_connection') as mock_get_conn:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [{"id": "EMP001"}]
            mock_conn.cursor.return_value = mock_cursor
            mock_conn.is_connected.return_value = True
            mock_get_conn.return_value = mock_conn
            
            success, result = execute_query("SELECT * FROM employees", fetchall=True)
            
            self.assertTrue(success)
            self.assertEqual(len(result), 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)