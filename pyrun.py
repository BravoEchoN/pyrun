import os
import tkinter as tk
from tkinter import messagebox
import subprocess

# Function to search for all Python files in the current directory, excluding this script
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

# Function to update the displayed files and folders based on the current directory
def update_display():
    for widget in frame_left.winfo_children():
        widget.destroy()
    for widget in frame_right.winfo_children():
        widget.destroy()

    # Display the parent directory button
    if os.getcwd() != start_directory:
        parent_button = tk.Button(frame_left, text=".. (Parent Directory)", command=lambda: change_directory('..'), fg='red')
        parent_button.pack(pady=5, fill=tk.X)

    # Display directories
    for item in os.listdir('.'):
        if os.path.isdir(item):
            button = tk.Button(frame_left, text=item, command=lambda d=item: change_directory(d), fg='red')
            button.pack(pady=5, fill=tk.X)

    # Display Python files
    col = 0
    row = 1
    max_cols = 6
    for item in os.listdir('.'):
        if item.endswith('.py') and item != os.path.basename(__file__):
            button = tk.Button(frame_right, text=item[:-3], command=lambda f=item: run_python_file(f), fg='blue')
            button.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

# Function to change the current directory
def change_directory(directory):
    os.chdir(directory)
    update_display()

# Create the main application window
root = tk.Tk()
root.title("Python Script Launcher")
root.geometry("800x300")

# Create frames for directories and scripts
frame_left = tk.Frame(root)
frame_left.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

separator = tk.Frame(root, width=2, bd=1, relief=tk.SUNKEN)
separator.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.Y)

frame_right = tk.Frame(root)
frame_right.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a label for directories
label_left = tk.Label(frame_left, text="Directories:")
label_left.pack(pady=10)

# Create a label for scripts
label_right = tk.Label(frame_right, text="Python Scripts:")
label_right.grid(row=0, columnspan=6, pady=10)

# Initialize the start directory
start_directory = os.getcwd()

# Display the initial directory contents
update_display()

# Start the GUI event loop
root.mainloop()
