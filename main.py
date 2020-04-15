# Name: Melvin Lin
# Software Project: Designing a CAD Tool for Logic Minimization

#                           main.py
# Purpose: The top level of the software project that contains the GUI 
# structure and incorporates the QM module that holds the 
# bulk of the Quine-McCluskey algorithm in the funQM module
#

from tkinter import * 
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.scrolledtext
import QM

filename = ''
content = ''

# Retrieves the filename 
def upload_filename(): 
    global filename
    filename = filedialog.askopenfile(mode ='r', filetypes =[('Plain Text Document', '*.txt')])

# Reads the content from the entry box
def read_input(): 
    global content
    content = expression.get()

# Error check to ensure that the boolean function is in the correct format
def error_check( value ): 
    if value.count('m') == 1 and value.count('+') == 0 and value.count('d') == 0:
        return False
    elif value.count('+') == 1 and value.count('d') == 1: 
        return False
    return True

# Clears the content of the entry box, so user's can try again
def clear_content(): 
    global content
    global filename
    content = ''
    filename = ''

    input.delete(0,END)

# Retrieves the contents in the file and displays error messages wherever 
# necessary
def retrieve_file_content( filename ): 
    text = ''
    if filename is not None: 
        content = filename.read().splitlines()
        if len(content) != 0: 
            for line in content: 
                value = QM.run(line)
                if (error_check(line) == True): 
                    messagebox.showerror("Error", "The boolean function is not formatted correctly! Try again by uploading a text file with the correct format or entering the correct format into the entry box.")
                    clear_content()
                    break
                text += line + "\n" + value + "\n" + "\n"
            return text
        else: 
            messagebox.showerror("Error", "No content in file! Try again by uploading a text file that has content.")
            clear_content()

# Displays error messages wherever the messages are needed
# Otherwise, the program will run as normal
def solve_booleans():
    global filename
    global content
    text = ''
    read_input()
    if content == '': 
        if filename == '': 
            messagebox.showerror("Error", "No content in entry box or in file! Try again by uploading a text file or entering boolean function into entry box.")
            clear_content()
        elif filename != '': 
            text = retrieve_file_content(filename)
            if text is not None: 
                output_window(text)
            else: 
                messagebox.showerror("Error", "No file was uploaded! Try again by uploading a text file or entering boolean function into entry box.")
            clear_content()
    else:  
        if filename != '': 
            messagebox.showerror("Error", "Only input a single boolean function or upload a .txt file, but not both.")
            clear_content()
        elif (error_check(content) == True):
            messagebox.showerror("Error", "The boolean function is not formatted correctly! Try again by uploading a text file with the correct format or entering the correct format into the entry box.")
            clear_content()
        else: 
            text += content + "\n"
            text += QM.run(content)
            text += "\n" + "\n"
            clear_content()
            output_window(text)

# Creates a new window for the outputs with the answers shown 
def output_window( text ): 
    output = Toplevel()
    output.title("Output")
    output.geometry("500x240")

    theme = Style()
    theme.theme_use('clam')

    output_header = Label(output, text='Outputs', font=("Impact", 35), background='white', foreground = 'black')
    output_header.pack()

    scrolledtext = tkinter.scrolledtext.ScrolledText(output)
    scrolledtext.pack(fill="both", expand=True)

    scrolledtext.insert(INSERT, text)
    scrolledtext.update_idletasks()
    scrolledtext.config(state=DISABLED)

# Creates a new window that describes the project and how to use it
def create_howto_window(): 
    howto = Toplevel()
    howto.title("Learn More")
    howto.geometry("500x240")

    theme = Style()
    theme.theme_use('clam')

    scrolledtext = tkinter.scrolledtext.ScrolledText(howto)
    scrolledtext.pack(fill="both", expand=True)

    credit_text = "Project Creator: Melvin Lin\nCreated on: April 4, 2020\n"
    scrolledtext.insert("end", credit_text, ("lefted",))
    scrolledtext.tag_configure("lefted", justify="left")

    scrolledtext.insert("end", "About\n\n", ("centered",))
    scrolledtext.tag_configure("centered", justify="center")

    about_text = "Logic Minimization is a CAD (computer-aided design) tool that is\nimplemented using the Quine-McCluskey algorithm to determine the\nminimized SOP (Sum-of-Products) and POS (Product-of-Sums)\nexpressions for the corresponding single-output Boolean functions.\nEach of the SOP and POS expressions can have up to 10\nliterals, meaning that the minterm range for the single-output\nBoolean function is 0 to 1023.\n\n" 
    scrolledtext.insert("end", about_text, ("centered",))
    scrolledtext.tag_configure("centered", justify="center")

    scrolledtext.insert("end", "How-to\n\n", ("centered",))
    scrolledtext.tag_configure("centered", justify="center")

    howto_text = "Hopefully, the Logic Minimization is fairly clear and intuitive in\nnature. But if it is not, this is what this section is for. The\nLogic Minimization takes in either a single-output Boolean function\ninto the entry box or a .txt file that has a single-output Boolean\nfunction or multiple single-output Boolean functions (each\nfollowed by a newline in file). The format of the single-output\nBoolean function should be\n\n"

    format_text = "m(1,2,3,4,5,6) + d(7,8,9).\n\n"

    howto_text2 = "After the entry box has been filled or the input file has been\nuploaded, the next step is to press the 'Click to Solve' button.\nThis button will lead to a pop-up screen that will show you\nthe SOP and POS expressions for each of the corresponding\nsingle-output Boolean functions.\n"

    scrolledtext.insert("end", howto_text, ("centered",))
    scrolledtext.tag_configure("centered", justify="center")
    scrolledtext.insert("end", format_text, ("centered",))
    scrolledtext.tag_configure("centered", justify="center")
    scrolledtext.insert("end", howto_text2, ("centered",))
    scrolledtext.tag_configure("centered", justify="center")

    scrolledtext.update_idletasks()
    scrolledtext.config(state=DISABLED)


# Styling and placement for the buttons, labels, and entry box that show up 
# on the starting page
master = Tk()
master.title("CAD Tool for Logic Minimization")
master.geometry("500x240")

style = Style()
style.theme_use('clam')

title = Label(master, text='Logic Minimization', font=("Impact", 45), background='white', foreground = 'black')
title.pack()

input_title = Label(master, text='Input Methods:', font=("Impact", 20), background='white', foreground = 'black')
input_title.pack(padx = (0, 350), pady = (10,0))

entry_description = Label(master, text='Enter Boolean Function [Format: m(1,2,3,4,5) + d(6,7,8)]:', font=("Aharoni", 10), background='white', foreground = 'black')
entry_description.pack(padx = (0, 150), pady = (5,0))

expression = StringVar()
input = Entry(master, width = 32, textvariable = expression)
input.pack(padx = (0, 150), pady = (0, 10))

or_statement = Label(master, text='OR', font=("Impact", 20), background='white', foreground = 'black')
or_statement.pack(padx = (0, 150), pady = (0,10))

file_button = Button(master, text='Upload File', command = lambda:upload_filename())
file_button.pack(padx = (0,150), pady = (0, 10))

learn_button = Button(master, text= 'Learn More', command = lambda: create_howto_window()).place(x = 355, y = 170)

solve_button = Button(master, text= 'Click to Solve',  command = lambda:solve_booleans()).place(x = 355, y = 130)

master.mainloop()