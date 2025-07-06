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
```

### 2. Setup Python Environment

Navigate into the orgChartApi directory and set up your Python environment.

```bash
# Optional: Create and activate a virtual environment
python3 -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# Install required Python libraries
pip install google-generativeai python-dotenv
```

### 3. Configrue Gemini API Key

The generate_tests.py script uses the Google Gemini API. You need to provide your API key.

Recommended Method (using .env file):
Create a new file named .env in the root of your orgChartApi directory (the same place as generate_tests.py). Add your API key to it:

```bash
# .env file
GOOGLE_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"
```
Replace "YOUR_ACTUAL_GEMINI_API_KEY_HERE" with your real API key.

### 4. Generate Unit Tests

Now, run the Python script to generate the C++ unit tests. Ensure you are in the orgChartApi root directory.

```bash
python generate_tests.py
```

## What to Expect:

The script will read the C++ files from the `src/` directory.

It will send this code, along with instructions, to the Gemini LLM.

The LLM will generate C++ unit test code.

A new directory named `tests/` will be created (if it doesn't exist).

The generated C++ unit tests will be saved in `tests/orgchart_unit_tests.cpp`.


## Note on LLM Output:
You might see a warning like `"Warning: No C++ code block found in LLM response. Returning raw text."` This means the LLM did not wrap the generated C++ code in Markdown fences (```cpp). The script will still save the raw output. You may need to manually open `tests/orgchart_unit_tests.cpp` and remove any non-C++ text  to make it a clean, compilable C++ file.
