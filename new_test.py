import platform
import subprocess

class Compiler:
    def __init__(self):
        self.os_type = platform.system().lower()
        print(f"Detected OS: {self.os_type}")  # Debugging step

        self.compiler_commands = {
            'python': {
                'windows': 'python',
                'linux': 'python3',
                'darwin': 'python3'  # macOS
            },
            'cpp': {
                'windows': 'g++.exe',  # Ensure g++ is accessible in PATH
                'linux': 'g++',
                'darwin': 'g++'
            }
        }

    def get_command(self, language):
        """Returns the appropriate command for the given language based on OS."""
        command = self.compiler_commands.get(language, {}).get(self.os_type, None)
        if not command:
            raise ValueError(f"Compiler not found for OS type: {self.os_type}")
        return command

    def compile_cpp(self, file_name):
        """Compiles a C++ file."""
        compiler = self.get_command('cpp')
        print(f"Using compiler: {compiler}")  # Debugging step

        output_file = file_name.split('.')[0]  # Remove file extension
        command = [compiler, '-std=c++17', '-o', output_file, file_name]

        try:
            subprocess.run(command, check=True)
            print(f"Compilation successful! Output file: {output_file}")
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed: {e}")

    def run_cpp(self, output_file):
        """Runs the compiled C++ binary."""
        executable = output_file if self.os_type == 'windows' else f"./{output_file}"
        print(f"Running executable: {executable}")  # Debugging step

        try:
            subprocess.run([executable], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Execution failed: {e}")


