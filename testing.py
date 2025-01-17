import subprocess
import os
import platform
import tempfile
import json
import logging
from new_test import Compiler
import time

class TestCaseHandler:
    def __init__(self):
        self.os_type = platform.system().lower()
        self.compiler_commands = {
            'python': {
                'windows': 'python',
                'linux': 'python3',
                'darwin': 'python3'  # macOS
            },
            'cpp': {
                'windows': 'g++.exe',
                'linux': 'g++',
                'darwin': 'g++'
            }
        }

    def create_temp_file(self, code: str, language: str) -> str:
       """Create a file with the code in the current working directory and return its name with extension."""
       if not code:
            raise ValueError("Code content cannot be empty")

       if language not in ['Python', 'Cpp']:
            raise ValueError("Unsupported language. Supported languages are 'Python' and 'Cpp'")

       ext = '.py' if language == 'Python' else '.cpp'

       try:
            # Generate a unique file name in the current working directory
            file_name = f"temp_{next(tempfile._get_candidate_names())}{ext}"
            file_path = os.path.join(os.getcwd(), file_name)

            # Write the code to the file
            with open(file_path, 'w') as f:
                f.write(code)

                return file_name  # Return just the file name
       except Exception as e:
            raise Exception(f"Failed to create file: {str(e)}")
        
    def create_temp_filepath(self, code: str, language: str) -> str:
        """Create a temporary file with the code."""
        if not code:
            raise ValueError("Code content cannot be empty")

        if language not in ['Python', 'Cpp']:
            print(language)
            raise ValueError("Unsupported language. Supported languages are 'Python' and 'Cpp'")

        ext = '.py' if language == 'Python' else '.cpp'

        try:
            with tempfile.NamedTemporaryFile(suffix=ext, mode='w', delete=False) as f:
                f.write(code)
                return f.name
        except Exception as e:
            raise Exception(f"Failed to create temporary file: {str(e)}")

    def compile_cpp(self, file_path: str) -> str:
        """Prepare and compile C++ code, returning the executable path."""
        # Ensure the file is saved as a `.cpp` file
        if not file_path.endswith('.cpp'):
            temp_cpp_path = os.path.join(os.getcwd(), 'temp_code.cpp')
            with open(file_path, 'r') as source_file:
                with open(temp_cpp_path, 'w') as cpp_file:
                    cpp_file.write(source_file.read())
            logging.info(f"File converted to C++ source: {temp_cpp_path}")
            file_path = temp_cpp_path
        

        # Determine the output executable path
        output_path = file_path.replace('.cpp', '.exe' if self.os_type == 'windows' else '.out')
        compiler_path = self.compiler_commands['cpp'].get(self.os_type)
        print(compiler_path)

        if not compiler_path or not os.path.isfile(compiler_path):
            raise FileNotFoundError(f"Compiler not found for OS type: {self.os_type}")

        # Compile the C++ file
        compile_cmd = [compiler_path, file_path, '-o', output_path]
        logging.debug(f"Compile command: {' '.join(compile_cmd)}")

        try:
            result = subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
            logging.debug(f"Compilation succeeded: {result.stdout}")
            return output_path
        except subprocess.CalledProcessError as e:
            logging.error(f"Compilation failed: {e.stderr}")
            raise Exception(f"Compilation error: {e.stderr}")

    def run_test_case(self, code: str, test_case: str, language: str) -> dict:
        """Run a test case and return the result."""
        compiler = Compiler()
        start_time = time.time()
        
        try:
            # Parse test case to separate input and expected output
            # Assuming format like "nums = [1,2,3], Output: 6"
            parts = test_case.split(", Output: ")
            input_data = parts[0]
            expected_output = parts[1].split(",")[0]  # Take first part in case there's an explanation

            # Prepare command based on language
            if language == 'Cpp':
                file_name = self.create_temp_file(code, language)
                executable = compiler.compile_cpp(file_name)
                cmd = [executable]
            elif language == 'Python':
                file_path = self.create_temp_filepath(code, language)
                cmd = [self.compiler_commands['python'][self.os_type], file_path]
            
            # Run the program
            process = subprocess.run(
                cmd,
                input=test_case,
                text=True,
                capture_output=True,
                timeout=5
            )
            
            execution_time = time.time() - start_time
            
            # Clean output by removing whitespace and newlines
            actual_output = process.stdout.strip()
            expected_output = str(expected_output).strip()
            
            # Validate output
            output_matches = self.validate_output(actual_output, expected_output)
            
            result = {
                'output': actual_output,
                'expected': expected_output,
                'error': process.stderr.strip(),
                'status': 'success' if (process.returncode == 0 and output_matches) else 'error',
                'execution_time': round(execution_time, 4),
                'output_matched': output_matches
            }
            
            # Log the test results
            self.log_test_result(test_case, expected_output, result)
                        
        except subprocess.TimeoutExpired:
            return {
                'output': '',
                'error': 'Timeout: Program execution exceeded 5 seconds',
                'status': 'timeout',
                'execution_time': 5.0,
                'output_matched': False
            }
        except Exception as e:
            return {
                'output': '',
                'error': str(e),
                'status': 'error',
                'execution_time': time.time() - start_time,
                'output_matched': False
            }
        
        finally:
            # Cleanup temporary files
            try:
                os.remove(file_path)
                if language == 'Cpp' and 'executable' in locals():
                    os.remove(executable)
            except:
                pass

        return result

    def validate_output(self, actual_output, expected_output):
        """
        Validates if the actual output matches the expected output.
        Handles different numeric formats and whitespace.
        """
        try:
            # Try to convert both to numbers if possible
            try:
                actual_num = float(actual_output)
                expected_num = float(expected_output)
                # Use almost equal for floating point comparisons
                return abs(actual_num - expected_num) < 1e-6
            except ValueError:
                pass
            
            # If not numbers, compare as strings after normalization
            actual_clean = ' '.join(actual_output.split())
            expected_clean = ' '.join(expected_output.split())
            return actual_clean == expected_clean
            
        except Exception:
            # If any error occurs during validation, return False
            return False

    def log_test_result(self, test_case, expected_output, result):
        """
        Logs the test results with detailed information about mismatches
        """
        logging.info(f"Test Case: Input: {test_case}")
        logging.info(f"Expected Output: {expected_output}")
        logging.info(f"Actual Output: {result['output']}")
        logging.info(f"Status: {result['status']}")
        logging.info(f"Execution Time: {result['execution_time']}s")
        
        if not result['output_matched']:
            logging.warning(f"Output Mismatch!")
            logging.warning(f"Expected: {expected_output}")
            logging.warning(f"Got: {result['output']}")
        
        if result['error']:
            logging.error(f"Error: {result['error']}")
                         
        

    def format_test_case(self, raw_test_case: str, problem_type: str) -> str:
        """Format test case based on problem type."""
        # Add custom formatting logic based on problem type
        # For example, array problems might need specific input formatting
        return raw_test_case

    def generate_test_cases(self, problem_info: dict) -> list:
        """Generate test cases from problem information."""
        test_cases = []
        
        # Extract example test cases from problem info
        for example in problem_info['examples']:
            test_cases.append(f"Input: {example['input']}, Output: {example['output']}, Explanation: {example.get('explanation', 'N/A')}")
        
        # Add sample test case if available
        if 'sampleTestCase' in problem_info:
            test_cases.append(problem_info['sampleTestCase'])

        # Format test cases based on problem type
        formatted_cases = []
        problem_type = problem_info.get('categoryTitle', '')
        
        for test in test_cases:
            if test.strip():  # Skip empty test cases
                formatted_cases.append(self.format_test_case(test, problem_type))

        return formatted_cases

    def run_all_tests(self, code: str, problem_info: dict, language: str) -> list:
        """Run all test cases for a problem."""
        test_cases = self.generate_test_cases(problem_info)
        print(test_cases)
        results = []
        
        for test_case in test_cases:
            result = self.run_test_case(code, test_case, language)
            results.append({
                'test_case': test_case,
                'result': result
            })

        return results