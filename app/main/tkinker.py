import tkinter as tk
from tkinter import messagebox

# Create the main window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Show the message box
response = messagebox.askyesno("Question", "Do you want to proceed?")

# Handle the response
if response:
    print("User selected Yes")
else:
    print("User selected No")

# Close the Tkinter window
root.quit()
