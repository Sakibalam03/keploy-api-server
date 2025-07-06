import google.generativeai as genai
import os
import yaml
import re

API_KEY = "your api key here"  # Replace with your actual API key or set it as an environment variable
if not API_KEY:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    exit(1)

genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-1.5-flash-latest"

CPP_SOURCE_DIR = "your-path-to-src"  # Replace with the actual path to your C++ source files
TESTS_OUTPUT_DIR = "tests"
TEST_FILE_NAME = "orgchart_unit_tests.cpp" 

INITIAL_PROMPT_YAML = """
task: generate_unit_tests
language: C++
framework: Google Test
requirements:
  - Generate comprehensive unit tests for the provided C++ classes and functions.
  - Focus on the core logic of classes like 'Employee' and 'OrgChart'.
  - Include tests for constructors, getters, setters, and logical operations.
  - For 'OrgChart', test adding/removing employees, finding employees, and hierarchical relationships.
  - Include basic positive test cases and relevant edge cases (e.g., empty chart, non-existent employees).
  - Ensure tests are well-structured, readable, and follow Google Test best practices.
  - Use appropriate Google Test macros (e.g., TEST, EXPECT_EQ, EXPECT_TRUE, EXPECT_FALSE, ASSERT_NE).
  - Include necessary #include directives (e.g., <gtest/gtest.h>, and your project's headers).
  - Output ONLY the C++ code for the unit tests. Do NOT include any explanations, markdown formatting (like ```cpp), or extra text.
  - The output should be a complete, compilable Google Test file.
"""

def read_cpp_files(directory):
    """Reads all .cpp and .h files from a given directory and its subdirectories."""
    cpp_files_content = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.cpp', '.h')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        cpp_files_content[file_path] = f.read()
                except Exception as e:
                    print(f"Warning: Could not read file {file_path}: {e}")
    return cpp_files_content

def generate_tests_with_llm(cpp_code_dict, prompt_yaml, model_name=MODEL_NAME):
    """Sends C++ code and prompt to LLM to generate unit tests."""
    model = genai.GenerativeModel(model_name)

    combined_cpp_code = ""
    for file_path, content in cpp_code_dict.items():
        combined_cpp_code += f"// File: {os.path.basename(file_path)}\n"
        combined_cpp_code += content
        combined_cpp_code += "\n\n"

    full_prompt = f"""
{prompt_yaml}

--- C++ Application Code ---
{combined_cpp_code}
"""
    print("Sending request to LLM...")
    try:

        response = model.generate_content(
            full_prompt,
            safety_settings={
                'HARASSMENT': 'BLOCK_NONE',
                'HATE': 'BLOCK_NONE',
                'SEXUAL': 'BLOCK_NONE',
                'DANGEROUS': 'BLOCK_NONE'
            }
        )

        generated_text = response.text
        print("LLM response received.")

        cpp_code_match = re.search(r'```(?:cpp|c\+\+)?\s*(.*?)\s*```', generated_text, re.DOTALL)
        if cpp_code_match:
            return cpp_code_match.group(1).strip()
        else:

            print("Warning: No C++ code block found in LLM response. Returning raw text.")
            return generated_text.strip()

    except Exception as e:
        print(f"Error generating content with LLM: {e}")

        if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
            print(f"Prompt Feedback: {response.prompt_feedback}")
        if hasattr(response, 'candidates') and response.candidates:
            for candidate in response.candidates:
                if hasattr(candidate, 'finish_reason'):
                    print(f"Candidate Finish Reason: {candidate.finish_reason}")
                if hasattr(candidate, 'safety_ratings'):
                    print(f"Candidate Safety Ratings: {candidate.safety_ratings}")
        return None

def save_generated_tests(test_code, output_dir, file_name):
    """Saves the generated test code to a file."""
    os.makedirs(output_dir, exist_ok=True) 
    file_path = os.path.join(output_dir, file_name)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(test_code)
        print(f"Generated unit tests saved to: {file_path}")
        return True
    except Exception as e:
        print(f"Error saving generated tests to {file_path}: {e}")
        return False

if __name__ == "__main__":
    print(f"Reading C++ files from: {CPP_SOURCE_DIR}")
    cpp_files = read_cpp_files(CPP_SOURCE_DIR)

    if not cpp_files:
        print(f"No C++ files found in {CPP_SOURCE_DIR}. Please ensure the 'src' directory exists and contains .cpp/.h files.")
        exit(1)

    print(f"Found {len(cpp_files)} C++ files.")

    generated_test_code = generate_tests_with_llm(cpp_files, INITIAL_PROMPT_YAML)

    if generated_test_code:
        save_generated_tests(generated_test_code, TESTS_OUTPUT_DIR, TEST_FILE_NAME)
    else:
        print("Failed to generate unit tests.")

