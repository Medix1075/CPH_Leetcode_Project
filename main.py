from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qsci import *
from PyQt5.QtGui import *
from pathlib import Path
import sys
import os
import subprocess
import logging
import json
from my_editor import Editor
from my_leetcode import LeetCodeApp
from testing import TestCaseHandler
from share_data import SharedData
from convert import convert_problem_to_json


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



class MainWindow(QMainWindow):
    def __init__(self):
        self.side_bar_clr = "#282c34"
        super(QMainWindow, self).__init__()
        self.init_ui()                                                  #Initialize UI
        self.leetcode_app = LeetCodeApp()

        self.current_file = None                                        #Placeholder for currently opened file
        self.current_side_bar = None
        self.file_compiler_mapping = {}                                 # {file_name: compiler}

    
        

    def init_ui(self):
        #Body
        self.setWindowTitle("Editor")
        self.resize(1300,900)

        self.setStyleSheet(open("C:/Users/Medhansh Jindal/OneDrive/Desktop/Python files/CPH_LeetCode_Project/style.qss","r").read())
 

        self.window_font = QFont("Fire Code")
        self.window_font.setPointSize(12)
        self.setFont(self.window_font)

        self.set_up_menu()
        self.set_up_body()
        
        self.statusBar().showMessage("Hellooo! Medhansh..")
        self.statusBar().setStyleSheet("""
                color: white; 
        """)

        

        self.show()

    def get_editor(self) -> QsciScintilla:
        editor = Editor()
        return editor

    
    def is_binary(self, path):
        '''
        Check if File is binary
        '''
        with open(path, 'rb') as f:
            return b'\0' in f.read(1024)
        
    def set_new_tab(self, path: Path, is_new_file=False):
        editor = self.get_editor()

        if is_new_file:
            self.tab_view.addTab(editor, "Untitled")
            self.setWindowTitle("Untitled")
            self.statusBar().showMessage("Opened Untitled")
            self.tab_view.setCurrentIndex(self.tab_view.count()-1)
            self.current_file = None

            # Default compiler for new files can be Python (or leave it undefined)
            self.file_compiler_mapping["Untitled"] = None
            return
            
        
        if not path.is_file():
            return
        if self.is_binary(path):
            self.statusBar().showMessage("Cannot Open Binary File", 2000)
            return
        
        #check if file is already open
        for i in range(self.tab_view.count()):
            if self.tab_view.tabText(i) == path.name:
                self.tab_view.setCurrentIndex(i)
                self.current_file = path
                return
                
        #Create New Tab
        self.tab_view.addTab(editor, path.name)
        if not is_new_file:
            editor.setText(path.read_text())
        self.setWindowTitle(path.name)
        self.current_file = path
        self.tab_view.setCurrentIndex(self.tab_view.count()-1)
        self.statusBar().showMessage(f"Opened {path.name}", 2000)

        # Set default compiler based on file extension
        if path.suffix == ".py":
            self.file_compiler_mapping[path.name] = "python"
        elif path.suffix in [".cpp", ".cxx", ".cc"]:
            self.file_compiler_mapping[path.name] = "cpp"
        else:
            self.file_compiler_mapping[path.name] = None


    def set_up_menu(self):
        menu_bar = self.menuBar()

        #File Menu
        file_menu = menu_bar.addMenu("File")

        new_file = file_menu.addAction("New")
        new_file.setShortcut("Ctrl+N")
        new_file.triggered.connect(self.new_file)

        open_file = file_menu.addAction("Open File")
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)

        file_menu.addSeparator()
        save_file = file_menu.addAction("Save")
        save_file.setShortcut("Ctrl+S")
        save_file.triggered.connect(self.save_file)

        save_file_as = file_menu.addAction("Save As")
        save_file_as.setShortcut("Ctrl+Shift+S")
        save_file_as.triggered.connect(self.save_as)

        open_folder = file_menu.addAction("Open Folder")
        open_folder.setShortcut("Ctrl+O")
        open_folder.triggered.connect(self.open_folder)

        #Edit Menu
        edit_menu = menu_bar.addMenu("Edit")

        copy_action = edit_menu.addAction("Copy")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)
        
        # Run button
        run_button = menu_bar.addMenu("Run Code")
        run_command = run_button.addAction("Run")
        run_command.triggered.connect(self.run_tests)

        #Compiler Menu
        compiler_menu = menu_bar.addMenu("Compiler")
        comp_python = compiler_menu.addAction("Python")
        comp_cpp = compiler_menu.addAction("C++")
        

        comp_python.triggered.connect(lambda: self.activate_compiler("Python"))
        comp_cpp.triggered.connect(lambda: self.activate_compiler("Cpp"))

        

    def activate_compiler(self, compiler_type):
        # Get the current tab index
        current_tab_index = self.tab_view.currentIndex()
        if current_tab_index == -1:
            QMessageBox.critical(self, "Error", "No file is currently open.")
            return

        # Get the file name or tab title
        file_name = self.tab_view.tabText(current_tab_index)

        # Update the compiler mapping for the current file/tab
        self.file_compiler_mapping[file_name] = compiler_type

        # Inform the user about the change
        QMessageBox.information(self, "Compiler Activated", 
                                    f"{compiler_type.capitalize()} compiler activated for {file_name}.")
        
        print(f"{compiler_type.capitalize()}")
        return f"{compiler_type.capitalize()}"
        


    # def run_current_file(self):
    #     # Get the current tab index
    #     current_tab_index = self.tab_view.currentIndex()
    #     if current_tab_index == -1:
    #         QMessageBox.critical(self, "Error", "No file is currently open.")
    #         return

    #     # Get the file name or tab title
    #     file_name = self.tab_view.tabText(current_tab_index)
    #     compiler = self.file_compiler_mapping.get(file_name)

    #     if compiler == "python":
    #         self.run_python_file(file_name)
    #     elif compiler == "cpp":
    #         self.run_cpp_file(file_name)
    #     else:
    #         QMessageBox.critical(self, "Error", f"No compiler is configured for {file_name}.")

    
    # def run_python_file(self, file_path):
    #     try:
    #         subprocess.run(["python", file_path], capture_output=True, text=True)
            
    #     except Exception as e:
    #         QMessageBox.critical(self, "Error", f"Failed to run Python file: {e}")

    # def run_cpp_file(self, file_path):
    #     output_executable = "output.exe"
    #     try:
    #         subprocess.run(["g++", file_path, "-o", output_executable], check=True)
    #         subprocess.run([output_executable], capture_output=True, text=True)
            
    #     except Exception as e:
    #         QMessageBox.critical(self, "Error", f"Failed to run C++ file: {e}")

        
    def load_problem_data(self, file_path):
        """Load problem data from a JSON file."""

        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            return None

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                logging.info("Problem data loaded successfully.")

                for key in ['description', 'examples', 'constraints']:
                    if key not in data:
                        logging.warning(f"Missing expected key: {key}")
                    else:
                        logging.debug(f"Key '{key}' found. Value type: {type(data[key])}")

                # Step 6: Return the data
                logging.info("Returning loaded data.")
                return data
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON: {e}")
            return None

    def run_tests(self):
        """Run tests for the active compiler."""
        if not self.activate_compiler:
            logging.error("No compiler is activated. Please select a compiler.")
            return

        # Get the code from the code editor
        current_editor = self.tab_view.currentWidget()
        if current_editor is None:
            logging.error("No active editor found!")
        else:
            submitted_code = current_editor.text()
            print(submitted_code)
        if not submitted_code.strip():
            logging.error("No code provided. Please enter code to run.")
            return

        # Load problem data
        share_data = SharedData ()
        content = share_data.problem_content
        content_json = convert_problem_to_json(content)
        problem_data = self.load_problem_data(content_json)
        if not problem_data:
            return

        # Initialize test case handler
        handler = TestCaseHandler()

        # Run all test cases
        test_results = handler.run_all_tests(submitted_code, problem_data, self.activate_compiler("Python"))

        # Display results in the console
        for result in test_results:
            status = result['result']['status']
            output = result['result'].get('output', "")
            error = result['result'].get('error', "")
            
            logging.info(f"Test Case: {result['test_case']}")
            logging.info(f"Status: {status}")
            if status == 'success':
                logging.info(f"Output: {output}")
            else:
                logging.error(f"Error: {error}")

    




    def new_file(self):
        self.set_new_tab(None, is_new_file=True)

    def save_file(self):
        # Check if there are any open tabs
        if self.tab_view.count() == 0:
            self.statusBar().showMessage("No open files to save.", 2000)
            return

        # Check if a file path is assigned; if not, call save_as()
        if self.current_file is None:
            self.save_as()  # Prompt the user to save the file with a new name
            if self.current_file is None:  # If user cancels save_as(), stop
                self.statusBar().showMessage("Save operation canceled.", 2000)
                return

        # Get the current editor (tab content)
        editor = self.tab_view.currentWidget()
        if editor is None or not hasattr(editor, "text"):
            self.statusBar().showMessage("Cannot save. Invalid editor instance.", 2000)
            return

        # Save the content to the file
        try:
            self.current_file.write_text(editor.text())
            self.statusBar().showMessage(f"Saved {self.current_file.name}", 2000)
        except Exception as e:
            self.statusBar().showMessage(f"Error saving file: {str(e)}", 2000)

    def save_as(self):
        editor = self.tab_view.currentWidget()
        if editor is None:
            return
        file_path = QFileDialog.getSaveFileName(self, "Save As", os.getcwd())[0]
        if file_path =='':
            self.statusBar().showMessage("Cancelled", 2000)
            return 
        
        path = Path(file_path)
        path.write_text(editor.text())
        self.tab_view.setTabText(self.tab_view.currentIndex(), path.name)
        self.statusBar().showMessage(f"Saved {path.name}", 2000)
        self.current_file = path


    def open_folder(self):
        ops = QFileDialog.Options()
        ops |= QFileDialog.DontUseNativeDialog

        new_folder = QFileDialog.getExistingDirectory(self, "Pick A Folder", "", options = ops)
        if new_folder:
            self.model.setRootPath(new_folder)
            self.tree_view.setRootIndex(self.model.index(new_folder))
            self.statusBar().showMessage(f"Opened {new_folder}", 2000)

    def open_file(self):
        ops = QFileDialog.Options()
        ops |= QFileDialog.DontUseNativeDialog
        new_file, _ = QFileDialog.getOpenFileName(self,
                    "Pick A File", "", "All Files (*);; Python Files(*.py)",
                    options = ops)
        if new_file == '':
            self.statusBar().showMessage("Cancelled", 2000)
            return 
        f = Path(new_file)
        self.set_new_tab(f)

    def copy(self):
        editor = self.tab_view.currentWidget()
        if editor is not None:
            editor.copy()


    def get_side_bar_label(self, path, name):
        label = QLabel()
        label.setPixmap(QPixmap(path).scaled(QSize(30, 30)))
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setFont(self.window_font)
        label.mousePressEvent = lambda e: self.show_hide_tab(e, name)
        label.enterEvent = self.set_cursor_pointer
        label.leaveEvent = self.set_cursor_arrow
        return label
    
    def set_cursor_arrow(self, event):
        self.setCursor(Qt.ArrowCursor)

    def set_cursor_pointer(self, event):
        self.setCursor(Qt.PointingHandCursor)

    def set_up_body(self):
        
        #Body
        body_frame = QFrame()
        body_frame.setFrameShape(QFrame.NoFrame)
        body_frame.setFrameShadow(QFrame.Plain)
        body_frame.setLineWidth(0)
        body_frame.setMidLineWidth(0)
        body_frame.setContentsMargins(0, 0, 0, 0)
        body_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body_frame.setLayout(body)

        #Split View
        self.hsplit = QSplitter(Qt.Horizontal)

        #sidebar
        self.side_bar = QFrame()
        self.side_bar.setFrameShape(QFrame.StyledPanel)
        self.side_bar.setFrameShadow(QFrame.Plain)
        self.side_bar.setMinimumWidth(50)
        self.side_bar.setStyleSheet(f'''
            background-color: {self.side_bar_clr};
        ''')
        side_bar_layout = QVBoxLayout()
        side_bar_layout.setContentsMargins(5, 20, 5, 0)
        side_bar_layout.setSpacing(20)
        side_bar_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)


        #setup labels
        
        folder_labels = self.get_side_bar_label("C:/Users/Medhansh Jindal/OneDrive/Desktop/Python files/CPH_LeetCode_Project/Icons/folder-icon-blue.svg", "folder-icon")
        leetcode_label = self.get_side_bar_label("C:/Users/Medhansh Jindal/OneDrive/Desktop/Python files/CPH_LeetCode_Project/Icons/leetcode.svg", "leetcode-label")        
        side_bar_layout.addWidget(folder_labels)
        side_bar_layout.addWidget(leetcode_label)

        self.side_bar.setLayout(side_bar_layout)


        #frame and layout to hold tree view (file manager)
        self.tree_frame = QFrame()
        self.tree_frame.setFrameShape(QFrame.NoFrame)
        self.tree_frame.setFrameShadow(QFrame.Plain)
        self.tree_frame.setLineWidth(1)
        self.tree_frame.setMaximumWidth(400)
        self.tree_frame.setMinimumWidth(200)
        self.tree_frame.setBaseSize(100, 0)
        self.tree_frame.setContentsMargins(0, 0, 0, 0)
        tree_frame_layout = QVBoxLayout()
        tree_frame_layout.setContentsMargins(0, 0, 0, 0)
        tree_frame_layout.setSpacing(0)
        self.tree_frame.setStyleSheet(''' 

            QFrame {
            background-color: #21252b;
            border-radius: 5px;
            border: None;
            color: #D3D3D3;
            padding: 5px;
            }
        
            QFrame:hover {
               color: white;
            }
         ''')
        
        #frame and layout to hold tree view (leetode problems)
        # self.leetcode_app.splitter = QFrame()
        # self.leetcode_app.splitter.setLineWidth(1)
        self.tree_frame.setFrameShape(QFrame.NoFrame)
        self.tree_frame.setFrameShadow(QFrame.Plain)
        # self.leetcode_app.splitter.setMaximumWidth(400)
        # self.leetcode_app.splitter.setMinimumWidth(200)
        # self.leetcode_app.splitter.setBaseSize(100, 0)
        # self.leetcode_app.splitter.setContentsMargins(0, 0, 0, 0)
        # self.leetcode_app.splitter = QVBoxLayout()
        # self.leetcode_app.splitter.setAlignment(Qt.AlignmentFlag.AlignTop)
        # self.leetcode_app.splitter.setContentsMargins(0, 10, 0, 0)
        # self.leetcode_app.splitter.setSpacing(0)
        # self.leetcode_app.splitter.setStyleSheet(''' 

        #     QFrame {
        #     background-color: #21252b;
        #     border-radius: 5px;
        #     border: None;
        #     color: #D3D3D3;
        #     padding: 5px;
        #     }
        
        #     QFrame:hover {
        #        color: white;
        #     }
        #  ''')
        
        problem_search_input = QLineEdit()
        problem_search_input.setPlaceholderText("Search Problem")
        problem_search_input.setFont(self.window_font)
        problem_search_input.setAlignment(Qt.AlignmentFlag.AlignTop)
        problem_search_input.setStyleSheet("""
         QLineEdit {
            background-color: #21252b;
            border-radius: 5px;
            border: 1px solid #D3D3D3;
            padding: 5px;
            color: #D3D3D3;                                
         }
         QLineEdit:hover {
            color: white;
           }
        """)

        self.check_box = QCheckBox("Search in Modules")
        self.check_box.setFont(self.window_font)
        self.check_box.setStyleSheet("color: white; margin-bottom: 10px;")

        #Problem Search View
        self.problem_list_view = QListWidget()
        self.problem_list_view.setFont(QFont("FiraCode", 13))
        self.problem_list_view.setStyleSheet("""
         QListWidget {
            background-color: #21252b;
            border-radius: 5px;
            border: 1px solid #D3D3D3;
            padding: 5px;
            color: #D3D3D3;                                 
                                             
            }
         QListWidget:hover {
                color: white;
            }   
        """)

        
        
        # self.leetcode_app.splitter.addSpacerItem(QSpacerItem(5,5, QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.problem_list_view.itemClicked.connect(self.problem_list_view_clicked)
        
        #Create file system model to show tree view
        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())

        #File System filters
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)

        #Tree View 
        self.tree_view = QTreeView()
        self.tree_view.setFont(QFont("FiraCode", 13))
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.getcwd()))
        self.tree_view.setSelectionMode(QTreeView.SingleSelection)
        self.tree_view.setSelectionBehavior(QTreeView.SelectRows)
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)

        #add custom context menu
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.tree_view_context_menu)

        #handling click
        self.tree_view.clicked.connect(self.tree_view_clicked)
        self.tree_view.setIndentation(10)
        self.tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #Hide Header and other columns other than name
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)



        #Setup Layout
        # self.leetcode_app.splitter.addWidget(problem_search_input)
        # self.leetcode_app.splitter.addWidget(self.problem_list_view)
        tree_frame_layout.addWidget(self.tree_view)
        self.tree_frame.setLayout(tree_frame_layout)
        # self.leetcode_app.splitter.setLayout(self.leetcode_app.splitter)

        #Adding a Tab View
        self.tab_view = QTabWidget()
        self.tab_view.setContentsMargins(0, 0, 0, 0)
        self.tab_view.setTabsClosable(True)
        self.tab_view.setMovable(True)
        self.tab_view.setDocumentMode(True)
        self.tab_view.tabCloseRequested.connect(self.close_tab)

        body.addWidget(self.side_bar)

        #add tree view and tab view
        self.hsplit.addWidget(self.tree_frame)
        # self.hsplit.addWidget(self.tree_frame_l)
        self.hsplit.addWidget(self.tab_view)

        body.addWidget(self.hsplit)
        
        body_frame.setLayout(body)
        
        self.setCentralWidget(body_frame)

    def problem_list_view_clicked(self):
        ...

    def show_hide_tab(self, e, type_):
        if type_ == "folder-icon":
            if not (self.tree_frame in self.hsplit.children()):
                self.hsplit.replaceWidget(0, self.tree_frame)
        elif type_ == "leetcode-label":
           if not (self.leetcode_app.splitter in self.hsplit.children()):
                self.hsplit.replaceWidget(0, self.leetcode_app.splitter) 

        if self.current_side_bar == type_:
            frame = self.hsplit.children()[0]
            if frame.isHidden():
                frame.show()
            else:
                frame.hide()

        self.current_side_bar = type_

    def tree_view_context_menu(self, pos):
        ...

    def tree_view_clicked(self, index: QModelIndex):
        path = self.model.filePath(index)
        p = Path(path)
        self.set_new_tab(p)

    def close_tab(self, index):
        self.tab_view.removeTab(index)

    # def run_tests(self):
    #     """Run tests for the current problem."""
    #     current_editor = self.tab_view.currentWidget()
    #     if not current_editor:
    #         return
    
    #     code = current_editor.text()
    #     tab_name = self.tab_view.tabText(self.tab_view.currentIndex())
    #     language = self.file_compiler_mapping.get(tab_name, 'python')
    
    #     # Get the current problem info
    #     if not hasattr(self, 'current_problem_info'):
    #         self.statusBar().showMessage("No problem selected", 2000)
    #         return
        
    #     test_handler = TestCaseHandler()
    #     results = test_handler.run_all_tests(code, self.current_problem_info, language)
    
    #     # Create and show test results in a new tab
    #     results_view = QTextBrowser()
    #     results_view.setStyleSheet("""
    #         QTextBrowser {
    #             background-color: #21252b;
    #             color: #D3D3D3;
    #             border: none;
    #             padding: 10px;
    #         }
    #     """)
    
    #     # Format results
    #     html_results = "<h2>Test Results</h2>"
    #     for i, test_result in enumerate(results, 1):
    #         status_color = "#4CAF50" if test_result['result']['status'] == 'success' else "#F44336"
    #         html_results += f"""
    #             <div style="margin-bottom: 15px;">
    #                 <h3 style="color: {status_color};">Test Case {i}</h3>
    #                 <pre style="background-color: #2C313C; padding: 10px;">Input:
    #     {test_result['test_case']}

    #     Output:
    #     {test_result['result']['output']}

    #     {"Error:" + test_result['result']['error'] if test_result['result'].get('error') else ''}
    #                 </pre>
    #             </div>
    #         """
    
    #     results_view.setHtml(html_results)
    #     self.tab_view.addTab(results_view, "🧪 Test Results")
    #     self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
        

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
