# Student Manager - Extension Problem
# This program reads student marks from a file, processes the data,
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import os

# Define the expected path to the student marks file
FILE_PATH = os.path.join("resources", "studentMarks.txt")

# --- Data Structure for Students ---
class Student:
    # Initializes a Student object with provided data and calculates totals, percentage, and grade.
    def __init__(self, code, name, c1, c2, c3, exam):
        # Raw Data
        self.code = code
        self.name = name
        self.c1 = int(c1)
        self.c2 = int(c2)
        self.c3 = int(c3)
        self.exam = int(exam)
        
        # Calculations
        self.coursework_total = self.c1 + self.c2 + self.c3 # Max 60
        self.overall_total = self.coursework_total + self.exam # Max 160
        self.percentage = (self.overall_total / 160) * 100
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        """Calculates the student's grade based on percentage."""
        # 'A' for 70%+, 'B' for 60%-69%, 'C' for 50%-59%, 'D' for 40%-49%, 'F' for under 40%
        if self.percentage >= 70:
            return 'A'
        elif 60 <= self.percentage < 70:
            return 'B'
        elif 50 <= self.percentage < 60:
            return 'C'
        elif 40 <= self.percentage < 50:
            return 'D'
        else:
            return 'F'

    def format_details(self):
        """Formats the student's results into a readable string."""
        return (
            f"Student Name: {self.name}\n"
            f"Student Number: {self.code}\n"
            f"Coursework Total: {self.coursework_total} / 60\n"
            f"Exam Mark: {self.exam} / 100\n"
            f"Overall Percentage: {self.percentage:.2f}%\n"
            f"Student Grade: {self.grade}\n"
            f"{'-' * 40}"
        )

# --- Main Application Class ---
class StudentApp:
    def __init__(self, master):
        self.master = master
        master.title("Student Marks Analyser")
        master.geometry("600x450")
        master.config(bg='#f0f0f0')

        # --- Data Storage ---
        self.students = self.load_data()
        self.num_students = len(self.students)
        
        # --- GUI Elements ---
        self.create_menu()
        self.create_output_area()
        self.display_welcome()

    # --- Data Loading and Parsing ---
    def load_data(self):
        """Loads data from the 'studentMarks.txt' file and parses it into Student objects."""
        students_list = []
        data_lines = []
        
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                data_lines = f.readlines()
        except FileNotFoundError:
            messagebox.showerror("File Not Found", 
                                f"FATAL ERROR: The required file '{FILE_PATH}' was not found. Please ensure it is in the correct location and restart the application.")
            return []
        except Exception as e:
            messagebox.showerror("Loading Error", f"An error occurred while reading the file: {e}")
            return []

        if not data_lines:
            messagebox.showwarning("Empty File", f"The file '{FILE_PATH}' is empty.")
            return []

        # Process subsequent lines (after the initial student count)
        for line in data_lines[1:]:
            parts = line.strip().split(',')
            if len(parts) == 6:
                try:
                    code, name, c1, c2, c3, exam = parts
                    students_list.append(Student(code.strip(), name.strip(), c1, c2, c3, exam))
                except ValueError:
                    # Skip lines with non-integer mark values
                    continue
        
        # Optional: Check if the loaded count matches the first line's count
        try:
            expected_count = int(data_lines[0].strip())
            if len(students_list) != expected_count:
                messagebox.showwarning("Data Mismatch", 
                                    f"WARNING: File header specified {expected_count} students, but only {len(students_list)} valid records were loaded.")
        except ValueError:
            messagebox.showwarning("Header Error", "WARNING: Could not parse the student count from the first line of the file.")

        return students_list

    # --- GUI Setup ---
    def create_menu(self):
        """Creates the main menu bar for the application."""
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        actions_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Actions", menu=actions_menu)
        
        # Menu Item 1
        actions_menu.add_command(label="1. View All Student Records", command=self.view_all_records)
        # Menu Item 2
        actions_menu.add_command(label="2. View Individual Student Record", command=self.view_individual_record)
        # Menu Item 3
        actions_menu.add_command(label="3. Show Highest Total Score", command=self.show_highest_score)
        # Menu Item 4
        actions_menu.add_command(label="4. Show Lowest Total Score", command=self.show_lowest_score)
        
        actions_menu.add_separator()
        actions_menu.add_command(label="Quit", command=self.master.destroy)

    def create_output_area(self):
        """Creates the main scrolled text area for displaying output."""
        output_frame = tk.Frame(self.master, padx=10, pady=10, bg='#ffffff')
        output_frame.pack(fill='both', expand=True)
        
        self.output_area = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, 
                                                    font=('Consolas', 10), 
                                                    bg='#EAEAEA', fg='#333333', 
                                                    padx=5, pady=5)
        self.output_area.pack(fill='both', expand=True)
        self.output_area.config(state=tk.DISABLED)

    def display_output(self, text):
        """Helper to safely insert text into the output area."""
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete('1.0', tk.END)
        self.output_area.insert(tk.END, text)
        self.output_area.config(state=tk.DISABLED)

    def display_welcome(self):
        """Displays a welcome message on startup."""
        if not self.students:
            self.display_output(
                "Welcome to the Student Marks Analyser!\n"
                "--------------------------------------\n"
                f"No student records were loaded. Please check that '{FILE_PATH}' exists and contains data."
            )
            return
            
        self.display_output(
            "Welcome to the Student Marks Analyser!\n"
            "--------------------------------------\n"
            f"Successfully loaded {self.num_students} student records.\n\n"
            "Use the 'Actions' menu above to select a task:\n"
            "1. View all student records\n"
            "2. View individual student record\n"
            "3. Show student with highest total score\n"
            "4. Show student with lowest total score"
        )

    # --- Menu Functionality ---
    
    # 1. View all student records
    def view_all_records(self):
        """Outputs all student records and class summary."""
        if not self.students:
            self.display_output("No student data available to view.")
            return

        all_details = "--- ALL STUDENT RECORDS ---\n"
        total_percentage_sum = 0
        
        for student in self.students:
            all_details += student.format_details()
            total_percentage_sum += student.percentage

        # Summary calculations
        average_percentage = total_percentage_sum / self.num_students if self.num_students > 0 else 0

        summary = (
            "\n--- CLASS SUMMARY ---\n"
            f"Number of Students in Class: {self.num_students}\n"
            f"Average Percentage Mark Obtained: {average_percentage:.2f}%\n"
            "---------------------"
        )
        
        self.display_output(all_details + summary)
        
    def view_individual_record(self):
        """Allows user to select a student by code or name and displays their record."""
        if not self.students:
            self.display_output("No student data available.")
            return

        search_term = simpledialog.askstring("Search Student", "Enter Student Code or Name:", 
                                            parent=self.master)
        
        if not search_term:
            return

        search_term = search_term.strip().lower()
        found_student = None

        for student in self.students:
            if student.code == search_term or student.name.lower() == search_term:
                found_student = student
                break
        
        if found_student:
            output = f"--- INDIVIDUAL STUDENT RECORD ---\n{found_student.format_details()}"
        else:
            output = f"Error: Student with code or name '{search_term}' not found."
            
        self.display_output(output)

    def show_highest_score(self):
        """Identifies and displays the student with the highest overall score."""
        if not self.students:
            self.display_output("No student data available to analyse.")
            return

        highest_student = max(self.students, key=lambda s: s.overall_total)

        output = (
            "--- STUDENT WITH HIGHEST TOTAL SCORE ---\n"
            f"Highest Score: {highest_student.overall_total} / 160\n"
            f"{'-' * 40}\n"
            f"{highest_student.format_details()}"
        )
        self.display_output(output)

    # 4. Show student with lowest overall mark
    def show_lowest_score(self):
        """Identifies and displays the student with the lowest overall score."""
        if not self.students:
            self.display_output("No student data available to analyse.")
            return

        lowest_student = min(self.students, key=lambda s: s.overall_total)

        output = (
            "--- STUDENT WITH LOWEST TOTAL SCORE ---\n"
            f"Lowest Score: {lowest_student.overall_total} / 160\n"
            f"{'-' * 40}\n"
            f"{lowest_student.format_details()}"
        )
        self.display_output(output)

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()