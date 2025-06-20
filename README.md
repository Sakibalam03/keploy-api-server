## Employee Management System

This repository contains a simple Employee Management System, featuring a Flask RESTful API as a backend and a pure HTML/JavaScript frontend. It allows for basic CRUD (Create, Read, Update, Delete) operations on employee data stored in a MySQL database.

## Table of Contents

1.  [Project Overview](#project-overview)
2.  [Database Setup](#database-setup)
    * [Database Details](#database-details)
    * [Database Schema](#database-schema)
3.  [Backend API (Flask)](#backend-api-flask)
    * [Functionality](#functionality)
    * [Dependencies](#dependencies)
    * [How to Run the Server](#how-to-run-the-server)
    * [API Endpoints](#api-endpoints)
        * [`POST /employees`](#post-employees) (Create Employee)
        * [`GET /employees`](#get-employees) (Read All Employees)
        * [`GET /employees/<employee_id>`](#get-employeesemployee_id) (Read Specific Employee)
        * [`PUT /employees/<employee_id>`](#put-employeesemployee_id) (Update Employee)
        * [`DELETE /employees/<employee_id>`](#delete-employeesemployee_id) (Delete Employee)
4.  [Frontend (HTML/JavaScript)](#frontend-htmljavascript)
    * [Functionality](#functionality-1)
    * [How to Run the Frontend](#how-to-run-the-frontend)
5.  [Interacting with the API (cURL Examples)](#interacting-with-the-api-curl-examples)
6.  [Troubleshooting](#troubleshooting)

---

## Project Overview

This application demonstrates a full-stack approach to managing employee records.
* **Backend:** A Python Flask application using a RESTful API to handle database interactions.
* **Database:** MySQL is used for storage of employee data.
* **Frontend:** A single HTML file with vanilla JavaScript provides a user interface to perform CRUD operations via the API.

## Database Setup

### Database Details

* **Type:** MySQL
* **Table Name:** `employees `
* **Integration:** The Flask backend connects to MySQL using the `mysql-connector-python` library.

### Database Schema

The `employees` table schema is defined as follows:

```sql
CREATE TABLE employees (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    emp_name VARCHAR(255) NOT NULL,
    joining_date DATE NOT NULL,
    project_id VARCHAR(50), -- Can be NULL
    mobile_no VARCHAR(20) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role ENUM('Employee', 'Manager', 'Admin') NOT NULL
);
````

**Table Constraints and Notes:**

  * `id`: `VARCHAR(50)`, `NOT NULL`, `PRIMARY KEY`.
  * `emp_name`: `VARCHAR(255)`, `NOT NULL`.
  * `joining_date`: `DATE`, `NOT NULL`. Dates should be in `YYYY-MM-DD` format.
  * `project_id`: `VARCHAR(50)`, can be `NULL`.
  * `mobile_no`: `VARCHAR(20)`, `NOT NULL`.
  * `email`: `VARCHAR(255)`, `UNIQUE`, `NOT NULL`. Each email must be unique in the table.
  * `role`: `ENUM`, `NOT NULL`. Can only be 'Employee', 'Manager', or 'Admin'.

## Backend API (Flask)

### Functionality

The Flask API (`app.py`) provides RESTful endpoints for performing all four CRUD operations on the `employees` table. It acts as the intermediary between the frontend and the MySQL database.

### Dependencies

To run the Flask API, you need the following Python libraries:

  * `Flask`
  * `mysql-connector-python`
  * `Flask-CORS` (for Cross-Origin Resource Sharing, allowing your frontend to communicate with the API)

Install them using pip:

```bash
pip install Flask mysql-connector-python Flask-CORS
```

### How to Run the Server

1.  **Configure Database:** Open `app.py` and update the `DB_CONFIG` dictionary with your actual MySQL database credentials:

    ```python
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root', # Your MySQL username
        'password': 'your_mysql_password', # Your MySQL password
        'database': 'your-db-name'
    }
    ```

2.  **Run the Flask App:** Navigate to the directory containing `app.py` in your terminal or command prompt and run:

    ```bash
    python app.py
    ```

    The server will start, typically on `http://127.0.0.1:5000/`. Keep this terminal window open as long as you want the API to be running.

### API Endpoints

All API requests expect and return `application/json`.

#### `POST /employees` (Create Employee)

  * **Description:** Adds a new employee record to the database.
  * **Method:** `POST`
  * **URL:** `http://localhost:5000/employees`
  * **Request Body (JSON):**
    ```json
    {
        "id": "EMP001",
        "emp_name": "Sakib Alam",
        "joining_date": "2024-01-01",
        "project_id": "PROJ001",
        "mobile_no": "8274828890",
        "email": "sarocks662@gmail.com",
        "role": "Employee"
    }
    ```
  * **Success Response (201 Created):**
    ```json
    {
        "message": "Employee added successfully",
        "id": "EMP001"
    }
    ```
  * **Error Response (400 Bad Request, 409 Conflict, 500 Internal Server Error):**
    ````json
    {
        "error": "Missing required fields (id, emp_name, joining_date, mobile_no, email, role)"
    }
    {
        "error": "Failed to add employee: ID 'EMP001' already exists."
    }
    ````

#### `GET /employees` (Read All Employees)

  * **Description:** Retrieves a list of all employee records.
  * **Method:** `GET`
  * **URL:** `http://localhost:5000/employees`
  * **Success Response (200 OK):**
    ```json
    [
        {
            "id": "EMP001",
            "emp_name": "Sakib Alam",
            "joining_date": "2024-01-01",
            "project_id": "PROJ001",
            "mobile_no": "8274828890",
            "email": "sarocks662@gmail.com",
            "role": "Employee"
        },
        {
            "id": "EMP002",
            "emp_name": "Saloni Chakraborty",
            "joining_date": "2025-05-10",
            "project_id": "PROJ002",
            "mobile_no": "9830646845",
            "email": "saloni.c@gmail.com",
            "role": "Employee"
        },
        {
            "id": "EMP003",
            "emp_name": "Priti Ranjan Sahoo",
            "joining_date": "2022-05-10",
            "project_id": "PROJ001",
            "mobile_no": "9876543210",
            "email": "pr.sahoo@gmail.com",
            "role": "Manager"
        },
        {
            "id": "EMP004",
            "emp_name": "Samaresh Mishra",
            "joining_date": "2021-05-10",
            "project_id": "NULL",
            "mobile_no": "9876213409",
            "email": "smishrafcs@gmail.com",
            "role": "Admin"
        }
    ]
    ```
  * **Error Response (500 Internal Server Error):**
    ```json
    {
        "error": "Failed to retrieve employees: [error_details]"
    }
    ```

#### `GET /employees/<employee_id>` (Read Specific Employee)

  * **Description:** Retrieves a single employee record by their ID.
  * **Method:** `GET`
  * **URL:** `http://localhost:5000/employees/EMP001` (replace `EMP001` with the actual ID)
  * **Success Response (200 OK):**
    ```json
    {
        "id": "EMP002",
        "emp_name": "Saloni Chakraborty",
        "joining_date": "2025-05-10",
        "project_id": "PROJ001",
        "mobile_no": "9830646845",
        "email": "saloni.c@gmail.com",
        "role": "Employee"
    }
    ```
  * **Error Response (404 Not Found):**
    ```json
    {
        "error": "Employee not found"
    }
    ```
  * **Error Response (500 Internal Server Error):**
    ```json
    {
        "error": "Failed to retrieve employee: [error_details]"
    }
    ```

#### `PUT /employees/<employee_id>` (Update Employee)

  * **Description:** Updates an existing employee record. Only provide the fields you want to change.
  * **Method:** `PUT`
  * **URL:** `http://localhost:5000/employees/EMP001` (replace `EMP001` with the ID of the employee to update)
  * **Request Body (JSON):**
    ```json
    {
        "emp_name": "Sakib Alam",
        "project_id": "PROJ002"
    }
    ```
    *(You can update one or more fields)*
  * **Success Response (200 OK):**
    ```json
    {
        "message": "Employee with ID EMP001 updated successfully"
    }
    ```
  * **Error Response (400 Bad Request, 500 Internal Server Error):**
    ```json
    {
        "error": "Enter fields to update."
    }
    ```

#### `DELETE /employees/<employee_id>` (Delete Employee)

  * **Description:** Deletes an employee record by their ID.
  * **Method:** `DELETE`
  * **URL:** `http://localhost:5000/employees/EMP001` (replace `EMP001` with the ID of the employee to delete)
  * **Success Response (200 OK):**
    ```json
    {
        "message": "Employee with ID EMP001 deleted successfully"
    }
    ```
  * **Error Response (500 Internal Server Error):**
    ```json
    {
        "error": "Failed to delete employee: [error_details]"
    }
    ```

## Frontend (HTML/JavaScript)

### Functionality

The `index.html` file provides a user-friendly interface to interact with the backend API. It includes:

  * A form with input fields for employee details.
  * Four distinct buttons for "Create Employee", "Read All Employees", "Update Employee", and "Delete Employee".
  * An `Employee ID` input field to specify which employee to update, delete, or retrieve individually.
  * A dynamic table that displays all employee records when "Read All Employees" is clicked.
  * Success and error message feedback.

### How to Run the Frontend

1.  **Ensure Server is Running:** Make sure your Flask API (`app.py`) is running (`python app.py`) and accessible at `http://localhost:5000`.
2.  **Open `index.html`:** Simply open the `index.html` file in your preferred web browser.
      * *(Note: Because of CORS, if you encounter issues, ensure `Flask-CORS` is installed and initialized in your `app.py` as `CORS(app)`).*

## Interacting with the API (cURL Examples)

You can use Postman to test the API directly.

**1. Create Employee (POST)**

```bash
curl -X POST \
  http://localhost:5000/employees \
  -H 'Content-Type: application/json' \
  -d '{
    "id": "EMP002",
    "emp_name": "Saloni Chakraborty",
    "joining_date": "2025-05-10",
    "project_id": "PROJ001",
    "mobile_no": "9830646845",
    "email": "saloni.c@gmail.com",
    "role": "Employee"
}'
```

**2. Read All Employees (GET)**

```bash
curl -X GET \
  http://localhost:5000/employees
```

**3. Read Specific Employee (GET)**

```bash
curl -X GET \
  http://localhost:5000/employees/EMP003
```

**4. Update Employee (PUT)**

```bash
curl -X PUT \
  http://localhost:5000/employees/EMP005 \
  -H 'Content-Type: application/json' \
  -d '{
    "emp_name": "Sakib Alam",
    "project_id": "PROJ002"
  }'
```

**5. Delete Employee (DELETE)**

```bash
curl -X DELETE \
  http://localhost:5000/employees/EMP003
```

## Troubleshooting

  * **`Error: Authentication plugin 'caching_sha2_password' is not supported`**: Update `mysql-connector-python` (`pip install --upgrade mysql-connector-python`) or change your MySQL user's authentication method to `mysql_native_password`.
  * **`Failed to create employee: Field 'id' doesn't have a default value`**: This means the `id` was not passed from the frontend to the backend during a `CREATE` operation. Ensure your `index.html` sends the `id` input value for `POST` requests and that `app.py` expects it.
  * **"Failed to fetch" or other network errors in the frontend**: Double-check that your Flask API (`app.py`) is actually running in a terminal, and that the `API_BASE_URL` in `index.html` (`http://localhost:5000`) matches where your Flask app is listening.
<!-- end list -->
