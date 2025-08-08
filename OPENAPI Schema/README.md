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
  - [Frontend](#frontend)  
- [API Reference](#api-reference)  
- [Keploy: Record/Replay Tests & CI](#keploy-recordreplay-tests--ci)  
- [CI/CD (GitHub Actions)](#cicd-github-actions)  
- [Troubleshooting](#troubleshooting)  
- [License](#license)

---

## Features

- CRUD for employees: **Create, Read, Update, Delete**
- **OpenAPI** docs via `flask-smorest` (Swagger UI)
- **CORS** enabled for local frontend ↔ backend dev
- **MySQL** persistence with unique email + primary key ID
- **Keploy** record-and-replay API tests (easy CI integration)

---

## Architecture

[Frontend (index.html)] → Fetch
│
▼
[Flask API (app.py)] → MySQL (employees table)
│
└─ Keploy (record test cases, replay in CI)

---

## Tech Stack

- **Backend:** Python 3, Flask, flask-smorest, Flask-CORS, mysql-connector-python  
- **DB:** MySQL 8+  
- **Frontend:** HTML + Vanilla JS  
- **Testing/CI:** Keploy CLI + GitHub Actions

---

## Project Structure

keploy-api-server/
├─ app.py # Flask API
├─ index.html # Minimal UI for CRUD
├─ OPENAPI Schema/ # OpenAPI schema + screenshots
├─ api-testing/ # Keploy API testing assets (if any)
├─ Unit Tests Generator/ # Keploy UT generator examples (if any)
└─ README.md


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
