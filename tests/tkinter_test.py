# Python program to create
# a file explorer in Tkinter

# import all components
# from the tkinter library
from tkinter import *

# import filedialog module
from tkinter import filedialog


# Function for opening the
# file explorer window
def browse_files():
    filename = filedialog.askopenfilename(initialdir="/home/emo",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      "*.*")))
    print(filename)


browse_files()
