import unittest
import json
import mysql.connector
from app import app

class TestEmployeeIntegration(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'your-user-password',
            'database': 'hrms_keploy_db'
        }
        
        # Test database connection
        try:
            connection = mysql.connector.connect(**cls.db_config)
            connection.close()
            print("Database connection successful")
        except Exception as e:
            raise Exception(f"Cannot connect to database: {e}")
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Test employee data
        self.test_employee = {
            "id": "TEST001",
            "emp_name": "Test Employee",
            "joining_date": "2024-01-15",
            "project_id": "PROJ_TEST",
            "mobile_no": "9999999999",
            "email": "sakib@gmail.com",
            "role": "Employee"
        }
        
        self.cleanup_test_data()
    
    def tearDown(self):
        self.cleanup_test_data()
    
    def cleanup_test_data(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()

            test_ids = ['TEST001', 'TEST002', 'TEST_UPDATE', 'TEST_DELETE']
            for test_id in test_ids:
                cursor.execute("DELETE FROM employees WHERE id = %s", (test_id,))
            
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Cleanup error: {e}")
    
    def get_employee_from_db(self, employee_id):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return result
        except Exception as e:
            print(f"Database query error: {e}")
            return None

    # CREATE (POST) Integration Tests
    def test_create_employee_integration(self):
        response = self.app.post('/employees',
                               data=json.dumps(self.test_employee),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn("Employee added successfully", response_data["message"])
        
        db_employee = self.get_employee_from_db("TEST001")
        self.assertIsNotNone(db_employee)
        self.assertEqual(db_employee["emp_name"], "Test Employee")
        self.assertEqual(db_employee["email"], "sakib@gmail.com")
        self.assertEqual(db_employee["role"], "Employee")
    
    def test_create_duplicate_employee_integration(self):
        response1 = self.app.post('/employees',
                                data=json.dumps(self.test_employee),
                                content_type='application/json')
        self.assertEqual(response1.status_code, 201)
        
        response2 = self.app.post('/employees',
                                data=json.dumps(self.test_employee),
                                content_type='application/json')
        
        self.assertIn(response2.status_code, [409, 500])
        response_data = json.loads(response2.data)
        self.assertIn("error", response_data)

    # READ (GET) Integration Tests
    def test_get_all_employees_integration(self):
        self.app.post('/employees',
                     data=json.dumps(self.test_employee),
                     content_type='application/json')
        
        response = self.app.get('/employees')
        
        self.assertEqual(response.status_code, 200)
        employees = json.loads(response.data)
        self.assertIsInstance(employees, list)
        
        test_employee_found = any(emp['id'] == 'TEST001' for emp in employees)
        self.assertTrue(test_employee_found)
    
    def test_get_employee_by_id_integration(self):

        self.app.post('/employees',
                     data=json.dumps(self.test_employee),
                     content_type='application/json')
        
        response = self.app.get('/employees/TEST001')
        
        self.assertEqual(response.status_code, 200)
        employee = json.loads(response.data)
        self.assertEqual(employee["id"], "TEST001")
        self.assertEqual(employee["emp_name"], "Test Employee")
        self.assertEqual(employee["email"], "sakib@gmail.com")
    
    def test_get_nonexistent_employee_integration(self):
        response = self.app.get('/employees/NONEXISTENT')
        
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data)
        self.assertIn("Employee not found", response_data["error"])

    def test_update_employee_integration(self):
        test_employee = self.test_employee.copy()
        test_employee["id"] = "TEST_UPDATE"
        
        self.app.post('/employees',
                     data=json.dumps(test_employee),
                     content_type='application/json')
        
        update_data = {
            "emp_name": "Updated Test Employee",
            "email": "sreyasjj@sakib.com",
            "role": "Manager"
        }
        
        response = self.app.put('/employees/TEST_UPDATE',
                              data=json.dumps(update_data),
                              content_type='application/json')
        

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("updated successfully", response_data["message"])
        
        db_employee = self.get_employee_from_db("TEST_UPDATE")
        self.assertIsNotNone(db_employee)
        self.assertEqual(db_employee["emp_name"], "Updated Test Employee")
        self.assertEqual(db_employee["email"], "sreyasjj@gmail.com")
        self.assertEqual(db_employee["role"], "Manager")
    
    def test_update_partial_employee_integration(self):
        test_employee = self.test_employee.copy()
        test_employee["id"] = "TEST002"
        
        self.app.post('/employees',
                     data=json.dumps(test_employee),
                     content_type='application/json')
        
        update_data = {"emp_name": "Partially Updated"}
        
        response = self.app.put('/employees/TEST002',
                              data=json.dumps(update_data),
                              content_type='application/json')
        

        self.assertEqual(response.status_code, 200)
        
        db_employee = self.get_employee_from_db("TEST002")
        self.assertEqual(db_employee["emp_name"], "Partially Updated")
        self.assertEqual(db_employee["email"], "sakib@gmail.com")  # Should remain same

    def test_delete_employee_integration(self):
        test_employee = self.test_employee.copy()
        test_employee["id"] = "TEST_DELETE"
        
        self.app.post('/employees',
                     data=json.dumps(test_employee),
                     content_type='application/json')
        

        db_employee = self.get_employee_from_db("TEST_DELETE")
        self.assertIsNotNone(db_employee)

        response = self.app.delete('/employees/TEST_DELETE')

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("deleted successfully", response_data["message"])

        db_employee = self.get_employee_from_db("TEST_DELETE")
        self.assertIsNone(db_employee)
    
    def test_delete_nonexistent_employee_integration(self):
        response = self.app.delete('/employees/NONEXISTENT')

        self.assertEqual(response.status_code, 200)

    def test_complete_crud_flow_integration(self):

        employee_id = "CRUD_FLOW"
        
        test_employee = self.test_employee.copy()
        test_employee["id"] = employee_id
        
        create_response = self.app.post('/employees',
                                      data=json.dumps(test_employee),
                                      content_type='application/json')
        self.assertEqual(create_response.status_code, 201)

        read_response = self.app.get(f'/employees/{employee_id}')
        self.assertEqual(read_response.status_code, 200)
        employee_data = json.loads(read_response.data)
        self.assertEqual(employee_data["emp_name"], "Test Employee")

        update_data = {"emp_name": "CRUD Updated Employee"}
        update_response = self.app.put(f'/employees/{employee_id}',
                                     data=json.dumps(update_data),
                                     content_type='application/json')
        self.assertEqual(update_response.status_code, 200)

        read_updated = self.app.get(f'/employees/{employee_id}')
        updated_data = json.loads(read_updated.data)
        self.assertEqual(updated_data["emp_name"], "CRUD Updated Employee")

        delete_response = self.app.delete(f'/employees/{employee_id}')
        self.assertEqual(delete_response.status_code, 200)

        read_deleted = self.app.get(f'/employees/{employee_id}')
        self.assertEqual(read_deleted.status_code, 404)

if __name__ == '__main__':
    unittest.main(verbosity=2)
