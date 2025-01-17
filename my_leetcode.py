from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QTreeWidget, QTreeWidgetItem, QSplitter, QLabel, QFrame, QTextEdit, QTextBrowser
)
from PyQt5.QtCore import Qt
import sys
from leetcode_api import *
from share_data import SharedData


class LeetCodeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LeetCode Problems")

        # Initialize API client
        try:
            self.client = get_user_info('Medix')  # Replace with dynamic username if needed
            if "data" not in self.client:
                raise ValueError("Invalid user info") 
        except Exception as e:
            print(f"Error initializing API client: {e}")
            self.client = None

        

        # Main Splitter (Tree View + Problem Details)
        self.splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.splitter)

        # Left Panel: Tree View for Categories
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemClicked.connect(self.on_tree_item_clicked)
        

        # Right Panel: Placeholder for Problem Details
        self.problem_table = QTableWidget()
        self.problem_table.setColumnCount(4)
        self.problem_table.setHorizontalHeaderLabels(["ID", "Title", "Difficulty", "Acceptance Rate"])
        self.problem_table.horizontalHeader().setFixedHeight(50)  # Adjust height to your preference
        self.problem_table.verticalHeader().setVisible(False)
        self.problem_table.setStyleSheet("""
            QHeaderView::section {
            background-color: #2c313c;
            color: #D3D3D3;
            border: 1px solid #3e4451;
            
        }
            QScrollBar:vertical {
            border: none;
            background: #2c313c;
            width: 10px;
            margin: 0px 0px 0px 0px;
        }
            QScrollBar::handle:vertical {
            background: #3e4451;
            min-height: 20px;
            border-radius: 5px;
        }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
            height: 0px;
        }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }

            QScrollBar:horizontal {
            border: none;
            background: #2c313c;
            height: 10px;
            margin: 0px 0px 0px 0px;
        }
            QScrollBar::handle:horizontal {
            background: #3e4451;
            min-width: 20px;
            border-radius: 5px;
        }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            border: none;
            background: none;
            width: 0px;
        }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }

            QTableCornerButton::section {
            background-color: #2c313c;
            border: 1px solid #3e4451;
            size: 10px;
        }
        """)
        self.problem_table.hide()  # Initially hidden
        

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
        
        # tree_frame_layout.addWidget(self.tree)
        # tree_frame_layout.addWidget(self.problem_table)
        # self.tree_frame.setLayout(tree_frame_layout)
        # self.splitter.addWidget(self.tree_frame)
        # self.splitter.addWidget(self.tree)
        # self.splitter.addWidget(self.problem_table)

        tree_frame_layout.addWidget(self.tree)
        tree_frame_layout.addWidget(self.problem_table)
        self.tree_frame.setLayout(tree_frame_layout)

        # Only add self.tree_frame to the splitter
        self.splitter.addWidget(self.tree_frame)

        # Modify the right panel to include problem details
        self.right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        # Problem details viewer
        self.problem_details = QTextBrowser()
        self.problem_details.setOpenExternalLinks(True)
        self.problem_details.setFrameShape(QFrame.StyledPanel)
        self.problem_details.setStyleSheet("""
            QTextBrowser {
                background-color: #21252b;
                color: #D3D3D3;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QScrollBar:vertical {
               border: none;
               background: #2c313c;
               width: 10px;
               margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #3e4451;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        right_layout.addWidget(self.problem_details)
        self.right_panel.setLayout(right_layout)
        self.right_panel.hide()

        # Connect table selection signal
        self.problem_table.itemSelectionChanged.connect(self.on_problem_selected)
        
        # Add the right panel to the splitter
        self.splitter.addWidget(self.right_panel)

        # Load Categories
        self.load_categories()

    def load_categories(self):
        """Load categories into the tree view."""
        categories = ["All Problems", "Difficulty", "Tags", "Companies", "Favorites"]

        for category in categories:
            parent = QTreeWidgetItem(self.tree, [category])
            if category == "Difficulty":
                for difficulty in ["Easy", "Medium", "Hard"]:
                    QTreeWidgetItem(parent, [difficulty])
            elif category == "Tags":
                for tag in ["Array", "Dynamic Programming", "Graph"]:
                    QTreeWidgetItem(parent, [tag])
            elif category == "Companies":
                for company in ["Google", "Facebook", "Amazon"]:
                    QTreeWidgetItem(parent, [company])

        self.tree.expandAll()

    def load_problems(self):
        """Fetch problems using the API and display in the table."""
        problems = self.fetch_leetcode_problems()

        if not problems:
            self.problem_table.setRowCount(1)
            self.problem_table.setItem(0, 0, QTableWidgetItem("No problems fetched. Check API or network."))
            return

        self.problem_table.setRowCount(len(problems))
        for row, problem in enumerate(problems):

            id_item = QTableWidgetItem(str(problem["stat"]["frontend_question_id"]))
            title_item = QTableWidgetItem(problem["stat"]["question__title"])

            acceptance_rate = problem["stat"]["total_acs"] / problem["stat"]["total_submitted"] * 100
            rate_item = QTableWidgetItem(f"{acceptance_rate:.2f} %")
            
            

            difficulty_map = {1: "Easy", 2: "Medium", 3: "Hard"}
            difficulty_level = difficulty_map.get(problem["difficulty"]["level"], "Unknown")
            difficulty_item = QTableWidgetItem(difficulty_level)

            if difficulty_level == "Hard":
                difficulty_item.setForeground(Qt.red)  # Set text color to red
                id_item.setForeground(Qt.red)
                title_item.setForeground(Qt.red)
                rate_item.setForeground(Qt.red)
            elif difficulty_level == "Medium":
                difficulty_item.setForeground(Qt.green)
                id_item.setForeground(Qt.green)
                title_item.setForeground(Qt.green)
                rate_item.setForeground(Qt.green)
            elif difficulty_level == "Easy":
                difficulty_item.setForeground(Qt.yellow)
                id_item.setForeground(Qt.yellow)
                title_item.setForeground(Qt.yellow)
                rate_item.setForeground(Qt.yellow)

            self.problem_table.setItem(row, 0, id_item)
            self.problem_table.setItem(row, 1, title_item)
            self.problem_table.setItem(row, 2, difficulty_item)
          
            self.problem_table.setItem(row, 3, rate_item)

    def fetch_leetcode_problems(self):
        """Fetch LeetCode problems using the Python API wrapper."""

        try:
            # Make an API request with a timeout using the `requests` library
            response = requests.get("https://leetcode.com/api/problems/all/", timeout=10)
            response.raise_for_status()  # Raise an error if the request fails
            problems = response.json()["stat_status_pairs"]  # Extract problem data
        
            # Validate response structure
            if not isinstance(problems, list):
                raise ValueError("Invalid response structure from the API.")
        
            return problems
        
        except requests.exceptions.Timeout:
            print("Error: API request timed out.")
            self.display_error_message("Error: API request timed out. Please try again.")
            return []
        
        except requests.exceptions.RequestException as e:
            # Log the error and inform the user
            print(f"Error fetching problems: {e}")
            self.display_error_message("Failed to fetch problems. Please check your network or API.")
            return []
        
        except KeyError:
            print("Error: Unexpected API response format.")
            self.display_error_message("Error: Unexpected API response format.")
            return []
       

    def fetch_problem_details(self, problem_slug):
        try:
            details = get_problem_info(problem_slug)
            if details and "content" in details:
                problem_statement = details["content"]
            else:
                problem_statement = "Failed to fetch problem details."
        
            self.problem_details.setText(problem_statement)
        except Exception as e:
            self.problem_details.setText(f"Error fetching problem details: {e}")

    def on_problem_selected(self):
        """Handle problem selection in the table."""
        selected_items = self.problem_table.selectedItems()
        if not self.right_panel.isVisible():
            self.right_panel.show()
        if not selected_items:
            return
        
        # Get the selected row
        row = self.problem_table.row(selected_items[0])
    
        # Get the problem title from the second column (index 1)
        problem_title = self.problem_table.item(row, 1).text()
    
        # Convert title to slug format (lowercase, hyphens instead of spaces)
        problem_slug = problem_title.lower().replace(' ', '-')
    
        # Fetch and display problem details
        problem_info = get_problem_info(problem_slug)
        if problem_info and "content" in problem_info:
            share_data = SharedData()
            share_data.problem_content = problem_info["content"]
            print(problem_info["content"])
            self.problem_details.setHtml(problem_info["content"])
            # Optionally display additional information
            difficulty = problem_info.get("difficulty", "Unknown")
            likes = problem_info.get("likes", 0)
            dislikes = problem_info.get("dislikes", 0)
        else:
            self.problem_details.setPlainText("Failed to load problem details.")

    

    def on_tree_item_clicked(self, item):
        """Handle tree item clicks to filter problems."""
        category = item.text(0)
        print(f"Selected Category: {category}")

        # Show the problem table if hidden
        if not self.problem_table.isVisible():
            self.problem_table.show()

        # Filter problems based on the selected category
        if category in ["Easy", "Medium", "Hard"]:
            self.filter_problems_by_difficulty(category)
        else:
            self.load_problems()  # Load all problems for other categories

    def filter_problems_by_difficulty(self, difficulty):
        """Filter problems by difficulty."""
        difficulty_map = {"Easy": 1, "Medium": 2, "Hard": 3}
        difficulty_level = difficulty_map[difficulty]

        problems = self.fetch_leetcode_problems()
        filtered_problems = [p for p in problems if p["difficulty"]["level"] == difficulty_level]

        self.update_problem_table(filtered_problems)

    def update_problem_table(self, problems):
        """Update the table with filtered problems."""
        if not problems:
            self.problem_table.setRowCount(1)
            self.problem_table.setItem(0, 0, QTableWidgetItem("No problems match the selected criteria."))
            return

        self.problem_table.setRowCount(len(problems))
        for row, problem in enumerate(problems):
            # Make items non-editable
            id_item = QTableWidgetItem(str(problem["stat"]["frontend_question_id"]))
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            
            title_item = QTableWidgetItem(problem["stat"]["question__title"])
            title_item.setFlags(title_item.flags() & ~Qt.ItemIsEditable)
            
            difficulty_map = {1: "Easy", 2: "Medium", 3: "Hard"}
            difficulty_level = difficulty_map.get(problem["difficulty"]["level"], "Unknown")
            difficulty_item = QTableWidgetItem(difficulty_level)
            difficulty_item.setFlags(difficulty_item.flags() & ~Qt.ItemIsEditable)
            
            acceptance_rate = problem["stat"]["total_acs"] / problem["stat"]["total_submitted"] * 100
            acceptance_item = QTableWidgetItem(f"{acceptance_rate:.2f} %")
            acceptance_item.setFlags(acceptance_item.flags() & ~Qt.ItemIsEditable)
            
            self.problem_table.setItem(row, 0, id_item)
            self.problem_table.setItem(row, 1, title_item)
            self.problem_table.setItem(row, 2, difficulty_item)
            self.problem_table.setItem(row, 3, acceptance_item)

        # Enable row selection
        self.problem_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.problem_table.setSelectionMode(QTableWidget.SingleSelection)


    def display_error_message(self, message):
        """Display an error message in the problem table."""
        self.problem_table.setRowCount(1)
        self.problem_table.setColumnCount(1)
        self.problem_table.setHorizontalHeaderLabels(["Error"])
        self.problem_table.setItem(0, 0, QTableWidgetItem(message))


if __name__ == "__main__":
    app = QApplication([])
    window = LeetCodeApp()
    window.show()
    sys.exit(app.exec_())



