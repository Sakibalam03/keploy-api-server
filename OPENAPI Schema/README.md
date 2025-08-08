# Employee Management API (Flask + MySQL) with OpenAPI & Keploy

A simple, end-to-end Employee Management system:

- **Backend:** Flask REST API with OpenAPI/Swagger (via `flask-smorest`), CORS, and MySQL.
- **Frontend:** Minimal HTML + JavaScript page for CRUD operations.
- **Testing:** Keploy test generation & CI integration.

> Live docs / details in this repo’s folders:
> - `app.py` (Flask API)  
> - `index.html` (UI)  

---

## Table of Contents

- [Features](#features)  
- [Architecture](#architecture)  
- [Tech Stack](#tech-stack)  
- [Project Structure](#project-structure)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Database Setup (MySQL)](#database-setup-mysql)  
  - [Backend Setup (Flask)](#backend-setup-flask)  
- [API Reference](#api-reference)  
- [Keploy: Record/Replay Tests & CI](#keploy-recordreplay-tests--ci)  
- [CI/CD (GitHub Actions)](#cicd-github-actions)  
- [Troubleshooting](#troubleshooting)  

---

## Features

- CRUD for employees: **Create, Read, Update, Delete**
- **OpenAPI** docs via `flask-smorest` (Swagger UI)
- **CORS** enabled for local frontend ↔ backend dev
- **MySQL** persistence with unique email + primary key ID
- **Keploy** record-and-replay API tests (easy CI integration)

---

## Architecture
```
[Frontend (index.html)] → Fetch
│
▼
[Flask API (app.py)] → MySQL (employees table)
│
└─ Keploy (record test cases, replay in CI)
```
---

## Tech Stack

- **Backend:** Python 3, Flask, flask-smorest, Flask-CORS, mysql-connector-python  
- **DB:** MySQL 8+  
- **Frontend:** HTML + Vanilla JS  
- **Testing/CI:** Keploy CLI + GitHub Actions

---

## Project Structure
```
keploy-api-server/
├─ OPENAPI Schema/
├─ app.py 
├─ index.html
├─ openapi.yaml
└─ README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+ (or your local version)
- MySQL 8+ running locally
- `pip` for Python dependencies

### Database Setup (MySQL)

Create a database and `employees` table:

```sql
CREATE DATABASE hrms_keploy_db;

USE hrms_keploy_db;

CREATE TABLE employees (
  id VARCHAR(50) NOT NULL PRIMARY KEY,
  emp_name VARCHAR(255) NOT NULL,
  joining_date DATE NOT NULL,
  project_id VARCHAR(50),          -- NULL allowed
  mobile_no VARCHAR(20) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  role ENUM('Employee','Manager','Admin') NOT NULL
);
```
Backend Setup (Flask)
Install dependencies:

```bash
pip install -r requirements.txt
# or
pip install Flask flask-smorest Flask-CORS mysql-connector-python marshmallow
```
Set DB credentials in app.py:
```
DB_CONFIG = {
  "host": "localhost",
  "user": "root",
  "password": "<your_password>",
  "database": "<database-name>"
}
```
API Reference
Base URL: Your hosted api URL

Create Employee
POST /employees
Body (JSON):
```
{
  "id": "EMP001",
  "emp_name": "Sakib Alam",
  "joining_date": "2025-06-21",     // YYYY-MM-DD
  "project_id": "PROJ001",
  "mobile_no": "9830646845",
  "email": "sakib.alam@gmail.com",
  "role": "Employee"
}
```
Success (201):
```
{ "message": "Employee added successfully", "id": "EMP001" }
```

List Employees
GET /employees

Returns an array of employees.

Get Employee by ID
GET /employees/{id}

Update Employee
PUT /employees/{id}
Body: include only fields to change, e.g.:
```
{ "project_id": "PROJ002", "role": "Manager" }
```
Delete Employee
DELETE /employees/{id}

##Keploy: Record/Replay Tests & CI
Keploy generates test cases + mocks from your real API calls, then replays them in CI.

![alt text][logo4]

[logo4]: https://github.com/Sakibalam03/keploy-api-server/blob/main/Assets/Keploy%20API%20Testing%20Dashboard.png "API Testing Dashboard"

Quick start (local):
```
# Install Keploy CLI
curl --silent -L https://keploy.io/ent/install.sh | bash

# 1) Start recording
keploy record -c "python app.py"

# 2) Use the app 

# 3) Replay
keploy test
```

![alt text][logo5]

[logo5]: https://github.com/Sakibalam03/keploy-api-server/blob/main/Assets/Keploy%20Website%20Extension%20for%20Project.png "Project Keploy API Testing"
CI/CD (GitHub Actions)

Create .github/workflows/ci.yml:
```
name: CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  keploy-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Start backend
        run: |
          nohup python app.py > server.log 2>&1 &
          # wait until the API is up
          for i in {1..30}; do
            if curl -sSf http://127.0.0.1:5000/employees >/dev/null; then
              echo "Server is up"; break
            fi
            sleep 1
          done

      - name: Install Keploy CLI
        run: |
          curl --silent -L https://keploy.io/ent/install.sh | bash
          keploy version

      - name: Run Keploy Test Suite
        env:
          KEPLOY_API_KEY: ${{ secrets.KEPLOY_API_KEY }}
        run: |
          keploy test-suite \
            --app=<YOUR_KEPLOY_APP_ID> \
            --base-path http://127.0.0.1:5000/employees \
            --cloud
```
Troubleshooting
* **`Failed to fetch`** from the browser:
  * Update `Ensure Flask is running and CORS is enabled.`
  * Update `Match exact URL/port between frontend and backend (use http://127.0.0.1:5000).`
  * Update `Avoid preflight redirects: prefer /employees (no trailing slash) and set app.url_map.strict_slashes = False.`
* **`CORS preflight 308 redirect`**:
  * Update `Serve routes without trailing slash or disable strict slashes.`
* **`MySQL connection errors`**:
  * Update `Verify credentials in DB_CONFIG, DB is running, and the employees table exists.`
* **`Date format issues`**:
  * Update `API expects YYYY-MM-DD for joining_date (unless you’ve added conversion logic).`
