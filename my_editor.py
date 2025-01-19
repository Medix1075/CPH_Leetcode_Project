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

        # Initialize both lexers
        self.pylexer = QsciLexerPython()
        self.cpp_lexer = QsciLexerCPP()
        
        # Set default font for both lexers
        self.pylexer.setDefaultFont(self.window_font)
        self.cpp_lexer.setDefaultFont(self.window_font)

        # Initialize APIs for both lexers
        self.api_py = QsciAPIs(self.pylexer)
        self.api_cpp = QsciAPIs(self.cpp_lexer)

        # Add Python keywords and built-ins
        for key in keyword.kwlist + dir(__builtins__):
            self.api_py.add(key)

        # Add Python modules
        for _, name, _ in pkgutil.iter_modules():
            self.api_py.add(name)

        # C++ keywords and built-ins
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

        # Add all C++ elements
        for key in cpp_keywords + cpp_functions + cpp_headers:
            self.api_cpp.add(key)

        # Prepare both APIs
        self.api_py.prepare()
        self.api_cpp.prepare()

        # Start with Python lexer by default
        self.setLexer(self.pylexer)

    def set_cpp_mode(self):
        self.setLexer(self.cpp_lexer)

    def set_python_mode(self):
        self.setLexer(self.pylexer)

        

    