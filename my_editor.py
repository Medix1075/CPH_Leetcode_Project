from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qsci import *
from PyQt5.QtGui import *
import keyword
import pkgutil

class Editor(QsciScintilla):
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)

        # Encoding
        self.setUtf8(True)

        # Font
        self.window_font = QFont("Fira Code")
        self.window_font.setPointSize(12)
        self.setFont(self.window_font)

        # Brace Matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Indentation
        self.setIndentationGuides(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(True)

        # Autocomplete
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)

        # Caret
        self.setCaretForegroundColor(QColor("dedcdc"))
        self.setCaretLineVisible(True)
        self.setCaretWidth(1)

        # EOL
        self.setEolMode(QsciScintilla.EolWindows)
        self.setEolVisibility(False)

        # Line Numbers
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "00000")
        self.setMarginsForegroundColor(QColor("#ff88888"))
        self.setMarginsBackgroundColor(QColor("#282c34"))
        self.setMarginsFont(self.window_font)

        # Set up Python Lexer
        self.pylexer = QsciLexerPython()
        self.pylexer.setDefaultFont(self.window_font)

        self.api = QsciAPIs(self.pylexer)
        for key in keyword.kwlist + dir(__builtins__):  # Add built-in functions and keywords
            self.api.add(key)

        for _, name, _ in pkgutil.iter_modules():  # Add module names from the current interpreter
            self.api.add(name)

        self.api.prepare()

        self.setLexer(self.pylexer)  # Use the Python lexer by default

    def set_cpp_mode(self):
        # Set up C++ Lexer
        self.cpp_lexer = QsciLexerCPP()
        self.cpp_lexer.setDefaultFont(self.window_font)

        self.api_cpp = QsciAPIs(self.cpp_lexer)
        cpp_keywords = [
            "int", "float", "double", "char", "void", "bool",
            "if", "else", "switch", "case", "for", "while", "do",
            "return", "break", "continue", "class", "struct", "namespace",
            "public", "private", "protected", "virtual", "template", "typename",
            "new", "delete", "try", "catch", "throw", "const", "static",
            "inline", "constexpr", "volatile", "operator", "friend", "this",
            "using", "namespace", "nullptr", "true", "false", "sizeof",
            "extern", "mutable", "typedef", "enum", "union", "goto",
        ]
        cpp_functions = [
            "std::cout", "std::cin", "std::endl",
            "std::vector", "std::string", "std::map",
            "std::set", "std::sort", "std::find",
            "std::sqrt", "std::pow", "std::abs",
            "std::getline", "std::to_string",
        ]
        cpp_headers = [
            "<iostream>", "<vector>", "<string>", "<map>", "<set>",
            "<cmath>", "<algorithm>", "<fstream>", "<sstream>", "<iomanip>",
        ]

        for key in cpp_keywords:
            self.api_cpp.add(key)

        for func in cpp_functions:
            self.api_cpp.add(func)

        for head in cpp_headers:
            self.api_cpp.add(head)

        self.api_cpp.prepare()

        self.setLexer(self.cpp_lexer)  # Switch to the C++ lexer

        

    