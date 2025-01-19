# Overview

This repository is designed to streamline competitive programming and LeetCode problem-solving workflows. It provides an automated and efficient environment for writing, compiling, and testing code across various programming languages like Python and C++.

# Features 

- **Custom Editor**: A PyQt5-based editor with syntax highlighting and autocompletion for Python and C++.
  
- **LeetCode API and CLI Integration**: Fetch problems directly from LeetCode, view problem details, and integrate solutions for efficient testing and debugging.

- **Test Case Automation**: Automatically handles test cases and verifies outputs.

- **Support for Multiple Languages**: Works seamlessly with Python and C++.

- **Code Compilation**: Integrates with g++ for C++ compilation and Python interpreters.

- **Cross-platform Support**: Works on Windows, Linux, and macOS.

- **Error Logging**: Detailed logging for debugging and error resolution.

# Requirements

To set up and run the project, ensure you have the following installed:

**General Requirements**

- Python 3.11.7 64-bit

- g++ Compiler (for C++)

- PyQt5 (for the editor)

- Qsci (for syntax highlighting and autocompletion)

# Installation

- **Clone the repository**:

       git clone https://github.com/Medix1075/CPH_Leetcode_Project.git
    
       cd CPH_Leetcode_Project

- Install the Requirements listed above.

- Set up the g++ compiler and ensure it is added to the system PATH.

- Run the editor or the script directly as needed.

# Usage

**Running the Editor**

The repository includes a PyQt5-based editor for editing and testing code. To run the editor:

     python main.py
     

**Writing and Testing Code**

Place your code in the designated Python or C++ script.

Use the test case handler to validate input/output against predefined cases.

# Logging

Logs are maintained to track errors and successful runs. They are stored in the current working directory for debugging purposes.
