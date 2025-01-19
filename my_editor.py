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

        # Initialize lexers
        self.pylexer = QsciLexerPython()
        self.cpp_lexer = QsciLexerCPP()
        
        # Set default font for lexers
        self.pylexer.setDefaultFont(self.window_font)
        self.cpp_lexer.setDefaultFont(self.window_font)

        # Create a single API for all keywords
        self.api = QsciAPIs(self.pylexer)  # Start with Python lexer's API

        # Add Python keywords and built-ins
        for key in keyword.kwlist + dir(__builtins__):
            self.api.add(key)

        # Add Python modules
        for _, name, _ in pkgutil.iter_modules():
            self.api.add(name)

        # C++ keywords and built-ins
        cpp_keywords = [
            "int", "float", "double", "char", "void", "bool",
            "if", "else", "switch", "case", "for", "while", "do",
            "return", "break", "continue", "class", "struct", "namespace",
            "public", "private", "protected", "virtual", "template", "typename",
            "new", "delete", "try", "catch", "throw", "const", "static",
            "inline", "constexpr", "volatile", "operator", "friend", "this",
            "using", "namespace", "nullptr", "true", "false", "sizeof",
            "extern", "mutable", "typedef", "enum", "union", "goto"
        ]

        cpp_functions = [
            "cout", "cin", "endl",  # Remove std:: prefix for easier use
            "vector", "string", "map",
            "set", "sort", "find",
            "sqrt", "pow", "abs",
            "getline", "to_string",
            # Add with std:: prefix
            "std::cout", "std::cin", "std::endl",
            "std::vector", "std::string", "std::map",
            "std::set", "std::sort", "std::find",
            "std::sqrt", "std::pow", "std::abs",
            "std::getline", "std::to_string"
        ]

        cpp_headers = [
            "iostream", "vector", "string", "map", "set",  # Without <>
            "cmath", "algorithm", "fstream", "sstream", "iomanip",
            # With <>
            "<iostream>", "<vector>", "<string>", "<map>", "<set>",
            "<cmath>", "<algorithm>", "<fstream>", "<sstream>", "<iomanip>"
        ]

        # Add C++ keywords to the same API
        for key in cpp_keywords + cpp_functions + cpp_headers:
            self.api.add(key)

        # Common programming constructs
        common_words = [
            "main", "print", "input", "output", "file", "read", "write",
            "open", "close", "start", "end", "next", "prev", "size", "length",
            "count", "index", "value", "key", "data", "node", "list", "array",
            "stack", "queue", "tree", "graph", "hash", "table"
        ]

        for word in common_words:
            self.api.add(word)

        # Prepare the API
        self.api.prepare()

        # Set initial lexer
        self.setLexer(self.pylexer)

    def set_cpp_mode(self):
        # Transfer the API to C++ lexer
        self.api = QsciAPIs(self.cpp_lexer)
        self.api.prepare()
        self.setLexer(self.cpp_lexer)

    def set_python_mode(self):
        # Transfer the API back to Python lexer
        self.api = QsciAPIs(self.pylexer)
        self.api.prepare()
        self.setLexer(self.pylexer)
        

    