import mysql.connector
from flask import Flask
from datetime import datetime
from flask_cors import CORS
from flask_smorest import Api, Blueprint, abort
from marshmallow import Schema, fields, validate

# --- Database Connection Parameters ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "sakib2003",
    "database": "hrms_keploy_db",
    # "auth_plugin": "mysql_native_password",
}

# -------------------- DB helpers --------------------
def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def execute_query(query, params=None, fetchone=False, fetchall=False):
    conn, cur = None, None
    try:
        conn = get_db_connection()
        if not conn:
            return False, "Database connection failed."

        cur = conn.cursor(dictionary=True)
        cur.execute(query, params)

        if query.strip().upper().startswith("SELECT"):
            if fetchone:
                data = cur.fetchone()
            elif fetchall:
                data = cur.fetchall()
            else:
                cur.fetchall()
                data = None
        else:
            conn.commit()
            data = cur.lastrowid

        return True, data
    except mysql.connector.Error as err:
        print(f"Database query error: {err}")
        if conn:
            conn.rollback()
        return False, str(err)
    finally:
        if cur:
            cur.close()
        if conn and conn.is_connected():
            conn.close()

def normalize_date_to_iso(datestr: str) -> str:
    """Accepts 'YYYY-MM-DD' or 'DD-MM-YYYY' and returns 'YYYY-MM-DD'."""
    if not datestr:
        raise ValueError("joining_date is required")
    for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(datestr.strip(), fmt).date().isoformat()
        except ValueError:
            pass
    raise ValueError("joining_date must be in 'YYYY-MM-DD' or 'DD-MM-YYYY' format")

def next_numeric_id() -> str:
    """Generate next numeric id as string (table uses VARCHAR PK)."""
    q = "SELECT MAX(CAST(id AS UNSIGNED)) AS max_id FROM employees"
    ok, res = execute_query(q, fetchone=True)
    if not ok:
        return "1"
    max_id = (res or {}).get("max_id")
    try:
        return str((int(max_id) if max_id is not None else 0) + 1)
    except Exception:
        return str(int(datetime.utcnow().timestamp()))

def is_truthy(v):
    return v is not None and str(v).strip() != ""

# -------------------- Schemas --------------------
class MessageSchema(Schema):
    message = fields.String(required=True)
    id = fields.String(required=False)

class EmployeeSchema(Schema):
    id = fields.String(required=False, allow_none=True)           # optional; auto-generate
    emp_name = fields.String(required=True)
    joining_date = fields.String(required=True)                   # we normalize manually
    project_id = fields.String(required=False, allow_none=True)
    mobile_no = fields.String(required=True)
    email = fields.Email(required=True)
    role = fields.String(required=True, validate=validate.OneOf(["Employee", "Manager", "Admin"]))

class EmployeeResponseSchema(Schema):
    id = fields.String()
    emp_name = fields.String()
    joining_date = fields.String()
    project_id = fields.String(allow_none=True)
    mobile_no = fields.String()
    email = fields.Email()
    role = fields.String()

class EmployeeUpdateSchema(Schema):
    emp_name = fields.String(required=False)
    joining_date = fields.String(required=False)
    project_id = fields.String(required=False, allow_none=True)
    mobile_no = fields.String(required=False)
    email = fields.Email(required=False)
    role = fields.String(required=False, validate=validate.OneOf(["Employee", "Manager", "Admin"]))

# -------------------- Flask app --------------------
def create_app():
    app = Flask(__name__)

    # IMPORTANT: avoid redirecting /employees -> /employees/
    app.url_map.strict_slashes = False

    # Make CORS explicit for preflight success
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=False,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        expose_headers=["Content-Type"],
        max_age=600,
    )

    # OpenAPI config
    app.config["API_TITLE"] = "Employee Management API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    api = Api(app)

    blp = Blueprint("Employees", "employees", url_prefix="/employees", description="Operations on employees")

    # ---------- CREATE ----------
    @blp.route("", methods=["POST"])  # <-- no trailing slash
    @blp.arguments(EmployeeSchema)
    @blp.response(201, MessageSchema, description="Employee created successfully")
    @blp.alt_response(400, description="Invalid input or missing fields")
    @blp.alt_response(409, description="Duplicate Employee ID or Email")
    def add_employee(new_employee_data):
        employee_id = new_employee_data.get("id")
        if not is_truthy(employee_id):
            employee_id = next_numeric_id()
        else:
            employee_id = str(employee_id).strip()

        emp_name = new_employee_data.get("emp_name", "").strip()
        try:
            joining_date_str = normalize_date_to_iso(new_employee_data.get("joining_date"))
        except ValueError as e:
            abort(400, message=str(e))

        project_id = new_employee_data.get("project_id")
        mobile_no = new_employee_data.get("mobile_no", "").strip()
        email = new_employee_data.get("email", "").strip()
        role = new_employee_data.get("role")

        if role not in ["Employee", "Manager", "Admin"]:
            abort(400, message="Invalid role. Must be 'Employee', 'Manager', or 'Admin'.")

        query = """
            INSERT INTO employees (id, emp_name, joining_date, project_id, mobile_no, email, role)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (employee_id, emp_name, joining_date_str, project_id, mobile_no, email, role)
        ok, res = execute_query(query, params)

        if ok:
            return {"message": "Employee added successfully", "id": employee_id}
        msg = str(res)
        if "Duplicate entry" in msg and ("for key 'PRIMARY'" in msg or "for key 'employees.PRIMARY'" in msg):
            abort(409, message=f"Failed to add employee: ID '{employee_id}' already exists.")
        if "Duplicate entry" in msg and ("for key 'email'" in msg or "for key 'employees.email'" in msg):
            abort(409, message=f"Failed to add employee: Email '{email}' already exists.")
        abort(500, message=f"Failed to add employee: {msg}")

    # ---------- READ ALL ----------
    @blp.route("", methods=["GET"])  # <-- no trailing slash
    @blp.response(200, EmployeeResponseSchema(many=True), description="List of all employees")
    def get_all_employees():
        ok, employees = execute_query("SELECT * FROM employees", fetchall=True)
        if ok:
            return employees, 200
        abort(500, message=f"Failed to retrieve employees: {employees}")

    # ---------- READ ONE ----------
    @blp.route("/<string:employee_id>", methods=["GET"])
    @blp.response(200, EmployeeResponseSchema, description="Specific employee details")
    @blp.alt_response(404, description="Employee not found")
    def get_employee_by_id(employee_id):
        ok, employee = execute_query("SELECT * FROM employees WHERE id = %s", (employee_id,), fetchone=True)
        if not ok:
            abort(500, message=f"Failed to retrieve employee: {employee}")
        if not employee:
            abort(404, message="Employee not found")
        return employee, 200

    # ---------- UPDATE ----------
    @blp.route("/<string:employee_id>", methods=["PUT"])
    @blp.arguments(EmployeeUpdateSchema)
    @blp.response(200, MessageSchema, description="Employee updated successfully")
    @blp.alt_response(400, description="Invalid input or no fields provided")
    @blp.alt_response(409, description="Duplicate Email")
    def update_employee(update_data, employee_id):
        if not update_data:
            abort(400, message="No fields provided for update")

        updates, params = [], []

        if "emp_name" in update_data:
            updates.append("emp_name = %s")
            params.append(update_data["emp_name"].strip())

        if "joining_date" in update_data and is_truthy(update_data["joining_date"]):
            try:
                jd = normalize_date_to_iso(update_data["joining_date"])
            except ValueError as e:
                abort(400, message=str(e))
            updates.append("joining_date = %s")
            params.append(jd)


        if "project_id" in update_data:
            updates.append("project_id = %s")
            params.append(update_data["project_id"])

        if "mobile_no" in update_data:
            updates.append("mobile_no = %s")
            params.append(update_data["mobile_no"].strip())

        if "email" in update_data:
            updates.append("email = %s")
            params.append(update_data["email"].strip())

        if "role" in update_data:
            role = update_data["role"]
            if role not in ["Employee", "Manager", "Admin"]:
                abort(400, message="Invalid role. Must be 'Employee', 'Manager', or 'Admin'.")
            updates.append("role = %s")
            params.append(role)

        if not updates:
            abort(400, message="No valid fields provided for update")

        q = f"UPDATE employees SET {', '.join(updates)} WHERE id = %s"
        params.append(employee_id)
        ok, res = execute_query(q, params)
        if ok:
            return {"message": f"Employee with ID {employee_id} updated successfully"}

        msg = str(res)
        if "Duplicate entry" in msg and ("for key 'email'" in msg or "for key 'employees.email'" in msg):
            abort(409, message=f"Failed to update employee: Email '{update_data.get('email')}' already exists.")
        abort(500, message=f"Failed to update employee: {msg}")

    # ---------- DELETE ----------
    @blp.route("/<string:employee_id>", methods=["DELETE"])
    @blp.response(200, MessageSchema, description="Employee deleted successfully")
    def delete_employee(employee_id):
        ok, res = execute_query("DELETE FROM employees WHERE id = %s", (employee_id,))
        if ok:
            return {"message": f"Employee with ID {employee_id} deleted successfully"}
        abort(500, message=f"Failed to delete employee: {res}")

    api.register_blueprint(blp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
