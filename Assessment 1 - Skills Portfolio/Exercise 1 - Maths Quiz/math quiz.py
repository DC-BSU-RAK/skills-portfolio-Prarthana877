# Arithmetic Adventure - A Math Quiz Game using Tkinter
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
# Define difficulty levels
DIFFICULTY = {1: (1, 9), 2: (10, 99), 3: (1000, 9999)}
# Main Game Class
class GameQuiz:
    # Initialize the game
    def __init__(self, root):
        # Store the root window
        self.root = root
        # Setup window
        self.root.title("Arithmetic Adventure")
        # Set initial size
        self.root.geometry("600x500")
        # Set minimum size
        self.root.minsize(400, 350)

        # Initialize game variables
        self.score = 0
        # Question counter
        self.question_count = 0
        # Attempt counter
        self.attempt = 1
        # Difficulty level
        self.difficulty = None
        # Current answer
        self.current_answer = None

        # Load images
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # Image paths
        self.bg_path = os.path.join(BASE_DIR, "IMAGES", "background.png")
        # Mushroom image path
        self.mushroom_path = os.path.join(BASE_DIR, "IMAGES", "mushroom.png")
        # Tree image path
        self.tree_path = os.path.join(BASE_DIR, "IMAGES", "tree.png")

        # Load images with fallback
        self.bg_orig = self.load_image(self.bg_path, (600, 500))
        # Load mushroom image
        self.mushroom_orig = self.load_image(self.mushroom_path, (50, 50))
        # Load tree image
        self.tree_orig = self.load_image(self.tree_path, (70, 70))

        # Setup canvas
        self.canvas = tk.Canvas(self.root)
        # Set canvas background
        self.canvas.pack(fill="both", expand=True)

        # Keep track of widgets for cleanup
        # This list will hold all the widgets we create
        self.widgets = []

        # Initial dimensions
        # Set initial dimensions
        self.width = 600
        # Set initial height
        self.height = 500

        # Bind resize event
        # This will allow the canvas to resize with the window
        self.root.bind("<Configure>", self.on_resize)
        
        # Show splash screen initially
        # Set current screen
        self.current_screen = "splash"
        # Display splash screen
        self.showSplashScreen()

    # Load image helper
    # This function loads an image from a file path and resizes it
    def load_image(self, path, default_size=(100,100)):
        # Try to open and resize the image
        try:
            # Open the image
            img = Image.open(path)
            # Resize the image
            return img
        # If loading fails, return a blank image
        except:
            # Log the error
            return Image.new("RGBA", default_size, (200,200,200,255))
        
    # Handle window resize
    def on_resize(self, event):
        # Check if the event is for the root window
        if event.widget == self.root:
            # Update dimensions
            self.width = max(event.width, 400)
            # Update height
            self.height = max(event.height, 350)
            # Redraw current screen
            if self.current_screen == "splash":
                # Show splash screen
                self.showSplashScreen()
            # Display menu screen
            elif self.current_screen == "menu":
                # Show menu screen
                self.displayMenu()
            # Display quiz problem
            elif self.current_screen == "quiz":
                # Show quiz problem
                self.displayProblem()
            # Display results screen
            elif self.current_screen == "results":
                # Show results screen
                self.displayResults()
    # Clear canvas and widgets
    def clearCanvas(self):
        # Clear the canvas
        self.canvas.delete("all")
        # Destroy all widgets
        for w in self.widgets:
            # Destroy widget
            w.destroy()
        # Clear widget list
        self.widgets.clear()

    # Calculate scaled font size
    # This function calculates a font size based on the current window width
    def scaled_font(self, factor, min_size=10, max_size=24):
        # Calculate size
        size = int(self.width * factor)
        # Return font tuple
        return ("Comic Sans MS", max(min_size, min(size, max_size)))

    # ---------------- Splash Screen ----------------
    # Show the splash screen
    # This function displays the splash screen
    def showSplashScreen(self):
        # Set current screen
        self.current_screen = "splash"
        # Clear canvas
        self.clearCanvas()
        # Resize and display background
        self.bg_image = ImageTk.PhotoImage(self.bg_orig.resize((self.width, self.height)))
        # Draw background image
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Display welcome text and instructions
        # Set fonts
        title_font = self.scaled_font(0.05, 14, 28)
        # Set text font
        text_font = self.scaled_font(0.025, 10, 18)

        # Title
        # Create title text
        self.canvas.create_text(self.width/2, 50, text="WELCOME TO ARITHMETIC ADVENTURE!",
                                font=title_font, fill="darkblue", justify="center")
        
        # Instructions
        # Create instruction text
        instructions = (
            # Instruction details
            "🧮 Solve 10 arithmetic problems.\n"
            # Scoring details
            "💡 Each correct answer gives 10 points on first try.\n"
            # Second attempt details
            "😅 Wrong once? Try again for 5 points.\n"
            # Final attempt details
            "❌ Two wrongs and you move on.\n\n"
            # Continue prompt
            "Click Continue to choose difficulty."
        )
        # Instruction text
        self.canvas.create_text(self.width/2, 180, text=instructions, font=text_font,
                                fill="black", justify="center", width=self.width*0.8)
        
        # Continue button
        # Create continue button
        continue_btn = tk.Button(self.root, text="Continue", font=text_font, bg="lightgreen",
                                command=self.displayMenu)
        # Add button to widgets list
        self.widgets.append(continue_btn)
        # Place button on canvas
        self.canvas.create_window(self.width/2, 300, window=continue_btn)

    # ---------------- Menu Screen ----------------
    # Display the menu screen
    def displayMenu(self):
        # Set current screen
        self.current_screen = "menu"
        # Clear canvas
        self.clearCanvas()
        # Resize and display background
        self.bg_image = ImageTk.PhotoImage(self.bg_orig.resize((self.width, self.height)))
        # Load and resize decorations
        self.mushroom_img = ImageTk.PhotoImage(self.mushroom_orig.resize((int(self.width*0.08), int(self.height*0.08))))
        # Load and resize tree image
        self.tree_img = ImageTk.PhotoImage(self.tree_orig.resize((int(self.width*0.12), int(self.height*0.12))))

        # Draw background and decorations
        # Draw background image
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        # Draw decorations
        self.canvas.create_image(0.05*self.width, 0.05*self.height, image=self.mushroom_img, anchor="nw")
        self.canvas.create_image(0.85*self.width, 0.05*self.height, image=self.mushroom_img, anchor="nw")
        self.canvas.create_image(0.05*self.width, 0.8*self.height, image=self.tree_img, anchor="nw")
        self.canvas.create_image(0.85*self.width, 0.8*self.height, image=self.tree_img, anchor="nw")

        # Difficulty selection
        # Create title and button fonts
        title_font = self.scaled_font(0.05, 14, 28)
        # Button font
        btn_font = self.scaled_font(0.03, 10, 20)
        # Title text
        self.canvas.create_text(self.width/2, 80, text="SELECT DIFFICULTY LEVEL", font=title_font, fill="darkblue")

        # Difficulty buttons
        # Easy button
        easy_btn = tk.Button(self.root, text="1. EASY", font=btn_font, bg="lightgreen", command=lambda: self.startQuiz(1))
        # Moderate button
        moderate_btn = tk.Button(self.root, text="2. MODERATE", font=btn_font, bg="yellow", command=lambda: self.startQuiz(2))
        # Advanced button
        advanced_btn = tk.Button(self.root, text="3. ADVANCED", font=btn_font, bg="pink", command=lambda: self.startQuiz(3))
        # Add buttons to widgets list
        self.widgets.extend([easy_btn, moderate_btn, advanced_btn])

        # Place buttons
        # Place easy button
        self.canvas.create_window(self.width/2, 180, window=easy_btn)
        # Place moderate button
        self.canvas.create_window(self.width/2, 250, window=moderate_btn)
        # Place advanced button
        self.canvas.create_window(self.width/2, 320, window=advanced_btn)

    # ---------------- Quiz Screen ----------------
    # Start the quiz
    def startQuiz(self, level):
        # Set difficulty level
        self.difficulty = level
        # Reset score
        self.score = 0
        # Reset question count
        self.question_count = 0
        # Reset attempt count
        self.attempt = 1
        # Display the first question
        self.nextQuestion()

    # Generate random integers based on difficulty
    def randomInt(self):
        # Get min and max values based on difficulty
        min_val, max_val = DIFFICULTY[self.difficulty]
        # Generate two random integers
        return random.randint(min_val, max_val), random.randint(min_val, max_val)

    # Decide operation (+ or -)
    def decideOperation(self):
        # Randomly choose an operation
        return random.choice(['+', '-'])
    
    # Display the current problem
    def displayProblem(self):
        # Set current screen
        self.current_screen = "quiz"
        # Clear canvas
        self.clearCanvas()
        # Resize and display background
        self.bg_image = ImageTk.PhotoImage(self.bg_orig.resize((self.width, self.height)))
        # Draw background image
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Generate problem
        # Get two random integers
        num1, num2 = self.randomInt()
        # Decide operation
        op = self.decideOperation()
        # Formulate question
        question = f"{num1} {op} {num2} ="
        # Calculate correct answer
        self.current_answer = eval(f"{num1} {op} {num2}")

        # Display question and input
        # Define fonts
        question_font = self.scaled_font(0.04, 12, 24)
        # Answer font
        entry_font = self.scaled_font(0.03, 10, 20)

        # Question text
        # Display question number
        self.canvas.create_text(self.width/2, 50, text=f"Question {self.question_count+1}", font=question_font, fill="black")
        # Display the question
        self.canvas.create_text(self.width/2, 120, text=question, font=question_font, fill="black")

        # Answer entry
        # Create entry widget for user input
        self.answer_entry = tk.Entry(self.root, font=entry_font, width=10)
        # Add entry widget to the list of widgets
        self.widgets.append(self.answer_entry)
        # Place entry widget on canvas
        self.canvas.create_window(self.width/2, 180, window=self.answer_entry)

        # Submit button
        # Create submit button
        submit_btn = tk.Button(self.root, text="Submit", font=entry_font, bg="lightblue", command=self.checkAnswer)
        # Add submit button to widgets list
        self.widgets.append(submit_btn)
        # Place submit button on canvas
        self.canvas.create_window(self.width/2, 240, window=submit_btn)

    # Check the submitted answer
    # Validate user input
    def checkAnswer(self):
        # Ensure answer entry is not empty
        try:
            # Get user answer
            user_answer = int(self.answer_entry.get())
        # Clear entry field
        except ValueError:
            messagebox.showerror("Oops!", "Enter a valid number.")
            return
        
        # Evaluate answer
        # Check if the answer is correct
        if user_answer == self.current_answer:
            # Update score based on attempt
            self.score += 10 if self.attempt == 1 else 5
            # Increment question count
            self.question_count += 1
            # Reset attempt count
            self.attempt = 1
        # If answer is incorrect
        else:
            # Provide feedback
            if self.attempt == 1:
                # Encourage user to try again
                messagebox.showinfo("Try Again", "Incorrect! Try once more.")
                # Increment attempt count
                self.attempt += 1
                # Provide encouragement
                return
            # Second incorrect attempt
            else:
                # Show correct answer
                messagebox.showinfo("Incorrect", f"The correct answer was {self.current_answer}.")
                # Increment question count
                self.question_count += 1
                # Reset attempt count
                self.attempt = 1

        # Proceed to next question or results
        # Check if there are more questions
        if self.question_count < 10:
            # Proceed to next question
            self.nextQuestion()
            # Display results
        else:
            # Show final results
            self.displayResults()

    # Go to next question
    # Display the next question
    def nextQuestion(self):
        # Reset answer entry
        self.displayProblem()

    # ---------------- Results Screen ----------------
    # Display the results
    def displayResults(self):
        # Show final results
        self.current_screen = "results"
        # Clear canvas
        self.clearCanvas()
        # Set background image
        self.bg_image = ImageTk.PhotoImage(self.bg_orig.resize((self.width, self.height)))
        # Add background image to canvas
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Define fonts
        # Title font
        title_font = self.scaled_font(0.05, 14, 28)
        # Text font
        text_font = self.scaled_font(0.03, 10, 22)
        # Button font
        btn_font = self.scaled_font(0.03, 10, 20)

        # Display results
        # Show final score and rank
        self.canvas.create_text(self.width/2, 50, text="Quiz Results", font=title_font, fill="black")
        # Show total questions attempted
        self.canvas.create_text(self.width/2, 120, text=f"Your final score: {self.score}", font=text_font, fill="black")
        # Show total questions attempted
        self.canvas.create_text(self.width/2, 150, text=f"Total questions attempted: {self.question_count}", font=text_font, fill="black")
        # Show correct answers
        self.canvas.create_text(self.width/2, 180, text=f"Your rank: {self.getGrade(self.score)}", font=text_font, fill="black")
        # Play again button
        replay_btn = tk.Button(self.root, text="Play Again", font=btn_font, bg="lightgreen", command=self.showSplashScreen)
        # Add button to widgets list
        self.widgets.append(replay_btn)
        # Place button on canvas
        self.canvas.create_window(self.width/2, 260, window=replay_btn)

    # Get grade based on score
    # Determine grade
    def getGrade(self, score):
        # Return grade based on score
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        else:
            return "D"
        
# Run the game
# Create the main application window
if __name__ == "__main__":
    # Initialize the main window
    root = tk.Tk()
    # Create game instance
    app = GameQuiz(root)
    # Start the Tkinter event loop
    root.mainloop()
