import os
import tkinter as tk
from tkinter import messagebox
import subprocess

# Function to search for all Python files in the working directory, excluding this script
def find_python_files():
    current_script = os.path.basename(__file__)
    return [f for f in os.listdir('.') if f.endswith('.py') and f != current_script]

# Function to run the selected Python file
def run_python_file(filename):
    try:
        result = subprocess.run(['python', filename], check=True, capture_output=True, text=True)
        output = result.stdout if result.stdout else "Script executed successfully with no output."
        log_output(filename, output)
        messagebox.showinfo("Output", output)
    except subprocess.CalledProcessError as e:
        error_message = f"An error occurred while running {filename}:\n{e.stderr}"
        log_output(filename, error_message)
        messagebox.showerror("Error", error_message)
    except Exception as e:
        error_message = f"Unexpected error:\n{str(e)}"
        log_output(filename, error_message)
        messagebox.showerror("Error", error_message)

# Function to log output and errors to a file
def log_output(filename, message):
    with open("script_launcher_log.txt", "a") as log_file:
        log_file.write(f"Output for {filename}:\n{message}\n{'-'*60}\n")

# Function to filter scripts based on search query
def filter_scripts(query):
    for button in button_list:
        if query.lower() in button['text'].lower():
            button.pack(pady=5, fill=tk.X)
        else:
            button.pack_forget()

# Create the main application window
root = tk.Tk()
root.title("Python Script Launcher")
root.geometry("400x600")

# Create a frame for the buttons
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a label
label = tk.Label(frame, text="Select a Python script to run:")
label.pack(pady=10)

# Create a search bar
search_var = tk.StringVar()
search_bar = tk.Entry(frame, textvariable=search_var)
search_bar.pack(pady=5, fill=tk.X)
search_bar.insert(0, "Search scripts...")

# Initialize the button list before defining the trace callback
button_list = []

# Search for Python files and create buttons
python_files = find_python_files()
for filename in python_files:
    button = tk.Button(frame, text=filename, command=lambda f=filename: run_python_file(f))
    button.pack(pady=5, fill=tk.X)
    button_list.append(button)

# Set up the trace callback for the search bar after initializing button_list
search_var.trace("w", lambda name, index, mode: filter_scripts(search_var.get()))

# Start the GUI event loop
root.mainloop()
