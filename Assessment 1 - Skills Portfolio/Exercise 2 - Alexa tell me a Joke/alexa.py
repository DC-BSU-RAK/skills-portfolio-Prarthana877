# Alexa Joke Telling Assistant
import tkinter as tk
from tkinter import messagebox
import random
import os

# Define the expected path to the joke file
FILE_PATH = os.path.join("resources", "randomJokes.txt")

# --- Application Class ---
# This class encapsulates the entire joke-telling application.
class JokeTellerApp:
    # Initialize the application with the main window (master)
    def __init__(self, master):
        # 1. Set up the main window
        self.master = master
        # Configure the main window's title, size, and padding
        master.title("😂 Joke Telling Assistant")
        # Set the window size to 550x300 pixels
        master.geometry("550x300")
        # Add padding around the window's content
        master.config(padx=20, pady=20)

        # 1. Load Jokes from File
        self.jokes = self.load_jokes_from_file(FILE_PATH)
        self.current_joke = ("", "") # Stores (setup, punchline)

        # 2. Joke Setup Label (Displays the question/setup)
        initial_text = "Click 'Alexa tell me a Joke' to begin!"
        # Handle case where no jokes were loaded
        if not self.jokes:
            # Display an error message if jokes could not be loaded
            initial_text = f"ERROR: Could not find or load jokes from '{FILE_PATH}'."
        
        # Create and configure the setup label
        self.setup_label = tk.Label(master, 
                                    text=initial_text, 
                                    font=('Arial', 14, 'italic'), 
                                    wraplength=500, justify=tk.LEFT)
        # Pack the setup label with padding and fill options
        self.setup_label.pack(pady=(10, 5), fill='x')

        # 3. Punchline Label (Displays the answer)
        self.punchline_label = tk.Label(master, 
                                        text="", 
                                        font=('Arial', 14, 'bold'), 
                                        fg='#007BFF',
                                        wraplength=500, justify=tk.LEFT)
        # Pack the punchline label with padding and fill options
        self.punchline_label.pack(pady=(0, 20), fill='x')

        # --- Button Frame for layout ---
        button_frame = tk.Frame(master)
        button_frame.pack(fill='x', pady=10)

        # 4. Initial Joke / Next Joke Button
        self.joke_button = tk.Button(button_frame, 
                                    text="Alexa tell me a Joke", 
                                    command=self.tell_new_joke, 
                                    bg='#28A745', fg='white', 
                                    font=('Arial', 10, 'bold'), width=18)
        # Pack the joke button with padding and expansion options
        self.joke_button.pack(side=tk.LEFT, padx=5, expand=True)
        
        # 5. Show Punchline Button
        self.punchline_button = tk.Button(button_frame, 
                                        text="Show Punchline", 
                                        command=self.show_punchline, 
                                        state=tk.DISABLED, 
                                        bg='#FFC107', fg='black', 
                                        font=('Arial', 10, 'bold'), width=18)
        # Pack the punchline button with padding and expansion options
        self.punchline_button.pack(side=tk.LEFT, padx=5, expand=True)

        # 6. Quit Button
        self.quit_button = tk.Button(master, 
                                    text="Quit", 
                                    command=master.destroy, 
                                    bg='#DC3545', fg='white', 
                                    font=('Arial', 10, 'bold'), width=10)
        # Pack the quit button with padding options
        self.quit_button.pack(pady=(10, 0))
    
    # --- Application Methods ---
    def load_jokes_from_file(self, file_path):
        """Attempts to load jokes from the specified file path."""
        jokes_list = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '?' in line:
                        try:
                            # Split only on the first question mark
                            setup, punchline = line.split('?', 1) 
                            jokes_list.append((setup.strip() + '?', punchline.strip()))
                        except ValueError:
                            # Skip lines that are malformed after the split
                            continue
            # Check if any jokes were loaded
            if not jokes_list:
                # Show error if no valid jokes were found
                messagebox.showerror("File Error", f"The file '{file_path}' was empty or contained no valid jokes.")
                # Return an empty list if no jokes were found
        except FileNotFoundError:
            # Show error if the file was not found
            messagebox.showerror("File Error", f"File not found: Please create the folder 'resources' and place 'randomJokes.txt' inside it.")
            # Return an empty list if the file was not found
        except Exception as e:
            # Show error for any other exceptions that may occur
            messagebox.showerror("Load Error", f"An unexpected error occurred while reading the file: {e}")
            # Return an empty list if an unexpected error occurred
        return jokes_list
    # --- Button Command Methods ---
    def tell_new_joke(self):
        """Randomly selects a new joke, displays the setup, and resets the view."""
        if not self.jokes:
            # Handle case where no jokes are available
            self.setup_label.config(text="No jokes available. Please check the 'randomJokes.txt' file. 🤷‍♀️")
            return

        # 1. Select and store new joke
        self.current_joke = random.choice(self.jokes)
        setup, _ = self.current_joke

        # 2. Display the setup
        self.setup_label.config(text=setup)

        # 3. Clear the punchline
        self.punchline_label.config(text="")

        # 4. Enable the "Show Punchline" button
        self.punchline_button.config(state=tk.NORMAL)
        
        # 5. Change the label to "Next Joke" after the initial click
        if self.joke_button['text'] == "Alexa tell me a Joke":
            self.joke_button.config(text="Next Joke")

    def show_punchline(self):
        """Displays the punchline for the current joke."""
        _, punchline = self.current_joke
        if punchline:
            self.punchline_label.config(text=punchline)
            # Disable the punchline button until a new joke is requested
            self.punchline_button.config(state=tk.DISABLED)
        else:
            self.punchline_label.config(text="🤔 Error: Click 'Next Joke' first.")

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = JokeTellerApp(root)
    root.mainloop()