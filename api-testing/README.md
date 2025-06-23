# Employee Management System - Testing Documentation

This document provides comprehensive testing information for the Employee Management System, covering both unit tests and integration tests. The testing suite ensures code quality, functionality verification, and database interaction validation for the Flask RESTful API backend.

## Table of Contents

1. [Testing Overview](#testing-overview)
2. [Unit Testing](#unit-testing)
   * [Test Coverage](#test-coverage)
   * [Dependencies](#dependencies)
   * [How to Run Unit Tests](#how-to-run-unit-tests)
   * [Test Categories](#test-categories)
       * [Mocking Scenarios](#mocking-scenarios)
       * [Non-Mocking Scenarios](#non-mocking-scenarios)
   * [Coverage Reports](#coverage-reports)
3. [Integration Testing](#integration-testing)
   * [Database Requirements](#database-requirements)
   * [How to Run Integration Tests](#how-to-run-integration-tests)
4. [Troubleshooting](#troubleshooting)

---

## Testing Overview

The testing suite for this Employee Management System is designed to ensure robust functionality and reliability through two complementary testing approaches:

* **Unit Testing:** Tests individual components and functions in isolation using mocking to simulate external dependencies.
* **Integration Testing:** Tests the complete system interaction between the Flask API and MySQL database with real data operations.

Both test suites use Python's built-in `unittest` framework for consistency and minimal external dependencies.


## Unit Testing

### Test Coverage

The unit testing suite achieves **82% code coverage** on the main application (`app.py`), exceeding the required 70% threshold. Coverage includes:

* API endpoint functionality
* Input validation and error handling
* Database connection management
* Request/response processing

### Dependencies

Unit tests use only built-in Python libraries:

* `unittest` (built-in testing framework)
* `unittest.mock` (for mocking external dependencies)
* `json` (for JSON data handling)
* `sys` (for module mocking)

**Optional dependency for coverage reporting:**
```bash
pip install coverage
```

How to Run Unit Tests
 **Basic Test Execution:**
  ```bash
  python test_app_unittest.py
```

With coverage report
```bash
python -m coverage run test_app_unittest.py
python -m coverage report -m
```

### Test Categories

#### Mocking Scenarios

These tests mock database interactions to focus on API logic:

* **Employee Creation Tests:**
 - Successful employee addition
 - Duplicate ID handling (409 Conflict)
 - Missing required fields validation
 - Invalid role validation

* **Employee Retrieval Tests:**
 - Get all employees successfully
 - Get specific employee by ID
 - Handle non-existent employee (404 Not Found)

* **Employee Update Tests:**
 - Successful employee updates
 - Validation of update fields

* **Employee Deletion Tests:**
 - Successful employee deletion

#### Non-Mocking Scenarios

These tests verify core functionality without external dependencies:

* **Database Connection Testing:**
 - Connection success scenarios
 - Connection failure handling

* **Input Validation:**
 - JSON parsing validation
 - Request format verification

* **Query Execution Testing:**
 - Different query types (SELECT, INSERT, UPDATE, DELETE)
 - Parameter binding
 - Result handling

### Coverage Reports

**Example Coverage Output:**
```bash
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
app.py                141     26    82%   38, 42-46, 50-54, 68, 102, 112, 126, 148-149, 153-154, 156-157, 159-160, 164-165, 168, 193
test_app_unittest.py   146      0   100%
-------------------------------------------------
TOTAL                 287     26    91%
```

## Integration Testing

### Database Requirements

Integration tests require a working MySQL database connection with the following setup:

* **Database:** `hrms_keploy_db`
* **Table:** `employees` (with schema as defined in main README)
* **Credentials:** Same as configured in `app.py`

**Note:** Tests use temporary test data with IDs like `TEST001`, `TEST_UPDATE`, etc., which are automatically cleaned up.

### How to Run Integration Tests

1. **Ensure Database is Running:**
   Make sure your MySQL server is running and accessible.

2. **Verify Database Connection:**
   Check that your `app.py` database configuration is correct.

3. **Run Integration Tests:**
   ```bash
   python test_integration.py
   ```
  ```bash
  Ran 10 tests in 1.633s
  OK (with 1 expected failure for duplicate handling)
  
  Database Operations Tested:
  - Employee Creation: ✅ PASSED
  - Employee Retrieval: ✅ PASSED  
  - Employee Updates: ✅ PASSED
  - Employee Deletion: ✅ PASSED
  - Complete CRUD Flow: ✅ PASSED
  ```

## Troubleshooting

### Integration Test Issues

**`Database connection failed`**
 - **Solution:** Verify MySQL server is running and accessible
 - **Check:** Confirm database credentials in `app.py` are correct
 - **Database:** Ensure `hrms_keploy_db` database exists

**`Table 'hrms_keploy_db.employees' doesn't exist`**
 - **Solution:** Create the employees table using schema from main README
 - **Command:** Run the CREATE TABLE statement from database setup

**`Failed test: test_create_duplicate_employee_integration`**
 - **Explanation:** Expected behavior - tests API's duplicate handling
 - **Status:** This may show as "expected failure" depending on API error response format
 - **Action:** Review API error handling in `app.py` if needed

**`Permission denied errors`**
 - **Solution:** Ensure MySQL user has INSERT, UPDATE, DELETE, SELECT permissions
 - **Check:** Verify database user privileges for test operations


**Testing Framework:** Python unittest  
**Coverage Tool:** coverage.py  
**Database:** MySQL 8.0+  
**Minimum Coverage:** 70% (Achieved: 82%)  
**Test Categories:** Unit Tests (Mocked) + Integration Tests (Real Database)
