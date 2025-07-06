# C++ Unit Test Generator for orgChartApi

This project provides a Python script to automatically generate C++ unit tests for the `orgChartApi` codebase using a Large Language Model (LLM). It's designed to automate the initial test generation phase, which can then be refined.

## Project Structure

* `generate_tests.py`: The Python script responsible for interacting with the LLM to generate tests.
* `src/`: Contains the source C++ files for the `orgChartApi` project (e.g., `Employee.cpp`, `OrgChart.cpp`, `main.cpp`, etc.).
* `tests/`: This directory will be created by the script, and the generated C++ unit test file (`orgchart_unit_tests.cpp`) will be saved here.

## Getting Started

Follow these steps to generate unit tests for the `orgChartApi` project.

### 1. Clone the `orgChartApi` Repository

First, ensure you have the `orgChartApi` project cloned to your local machine.

```bash
git clone [https://github.com/keploy/orgChartApi.git](https://github.com/keploy/orgChartApi.git)
cd orgChartApi