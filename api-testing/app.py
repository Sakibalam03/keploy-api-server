import mysql.connector
from flask import Flask, request, jsonify
from datetime import date, datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', 
    'password': 'sakib2003', 
    'database': 'hrms_keploy_db' 

}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def execute_query(query, params=None, fetchone=False, fetchall=False):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return False, "Database connection failed."

        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)

        if query.strip().upper().startswith("SELECT"):
            if fetchone:
                result_data = cursor.fetchone()
            elif fetchall:
                result_data = cursor.fetchall()
            else:
                cursor.fetchall() 
                result_data = None 
        else:
            connection.commit() 
            result_data = cursor.lastrowid 

        return True, result_data

    except mysql.connector.Error as err:
        print(f"Database query error: {err}")
        if connection:
            connection.rollback()
        return False, str(err)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# --- API Endpoints ---

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data provided"}), 400

    employee_id = data.get('id') 
    emp_name = data.get('emp_name')
    joining_date_str = data.get('joining_date')
    project_id = data.get('project_id')
    mobile_no = data.get('mobile_no')
    email = data.get('email')
    role = data.get('role')

    if not all([employee_id, emp_name, joining_date_str, mobile_no, email, role]):
        return jsonify({"error": "Missing required fields (id, emp_name, joining_date, mobile_no, email, role)"}), 400

    try:
        joining_date = datetime.strptime(joining_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format for joining_date. Use YYYY-MM-DD."}), 400

    if role not in ['Employee', 'Manager', 'Admin']:
        return jsonify({"error": "Invalid role. Must be 'Employee', 'Manager', or 'Admin'."}), 400

    query = """
    INSERT INTO employees (id, emp_name, joining_date, project_id, mobile_no, email, role)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (employee_id, emp_name, joining_date, project_id, mobile_no, email, role)

    success, result = execute_query(query, params)

    if success:
        return jsonify({"message": "Employee added successfully", "id": employee_id}), 201
    else:
        if "Duplicate entry" in result and "for key 'PRIMARY'" in result:
             return jsonify({"error": f"Failed to add employee: ID '{employee_id}' already exists."}), 409 # Conflict
        return jsonify({"error": f"Failed to add employee: {result}"}), 500

@app.route('/employees', methods=['GET'])
def get_all_employees():
    query = "SELECT * FROM employees"
    success, employees = execute_query(query, fetchall=True)

    if success:
        for emp in employees:
            if 'joining_date' in emp and isinstance(emp['joining_date'], date):
                emp['joining_date'] = emp['joining_date'].isoformat()
        return jsonify(employees), 200
    else:
        return jsonify({"error": f"Failed to retrieve employees: {employees}"}), 500

@app.route('/employees/<string:employee_id>', methods=['GET']) # Changed to string
def get_employee_by_id(employee_id):
    query = "SELECT * FROM employees WHERE id = %s"
    params = (employee_id,)
    success, employee = execute_query(query, params, fetchone=True)

    if success:
        if employee:
            if 'joining_date' in employee and isinstance(employee['joining_date'], date):
                employee['joining_date'] = employee['joining_date'].isoformat()
            return jsonify(employee), 200
        else:
            return jsonify({"error": "Employee not found"}), 404
    else:
        return jsonify({"error": f"Failed to retrieve employee: {employee}"}), 500

@app.route('/employees/<string:employee_id>', methods=['PUT']) # Changed to string
def update_employee(employee_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data provided"}), 400

    updates = []
    params = []

    if 'emp_name' in data:
        updates.append("emp_name = %s")
        params.append(data['emp_name'])
    if 'joining_date' in data:
        try:
            joining_date = datetime.strptime(data['joining_date'], '%Y-%m-%d').date()
            updates.append("joining_date = %s")
            params.append(joining_date)
        except ValueError:
            return jsonify({"error": "Invalid date format for joining_date. Use YYYY-MM-DD."}), 400
    if 'project_id' in data:
        updates.append("project_id = %s")
        params.append(data['project_id'])
    if 'mobile_no' in data:
        updates.append("mobile_no = %s")
        params.append(data['mobile_no'])
    if 'email' in data:
        updates.append("email = %s")
        params.append(data['email'])
    if 'role' in data:
        if data['role'] not in ['Employee', 'Manager', 'Admin']:
            return jsonify({"error": "Invalid role. Must be 'Employee', 'Manager', or 'Admin'."}), 400
        updates.append("role = %s")
        params.append(data['role'])

    if not updates:
        return jsonify({"message": "No fields provided for update"}), 400

    query = f"UPDATE employees SET {', '.join(updates)} WHERE id = %s"
    params.append(employee_id)

    success, result = execute_query(query, params)

    if success:
        return jsonify({"message": f"Employee with ID {employee_id} updated successfully"}), 200
    else:
        return jsonify({"error": f"Failed to update employee: {result}"}), 500

@app.route('/employees/<string:employee_id>', methods=['DELETE']) # Changed to string
def delete_employee(employee_id):
    query = "DELETE FROM employees WHERE id = %s"
    params = (employee_id,)
    success, result = execute_query(query, params)

    if success:
        return jsonify({"message": f"Employee with ID {employee_id} deleted successfully"}), 200
    else:
        return jsonify({"error": f"Failed to delete employee: {result}"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
