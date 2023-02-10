import tkinter as tk
from tkinter import *
from load_page import InputLoadPage
from computing_page import ComputingPage

class SelectOperationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        selection_prompt = Label(self, text = "Please select an operation")
        selection_prompt.place(relx=.5, rely=.1, anchor= CENTER)

        load_button = Button(self, text="Load/Unload", command=lambda: controller.show_frame(InputLoadPage), width=20)
        load_button.place(relx=.25, rely=.2, anchor= CENTER)        
        balance_button = Button(self, text="Balance", command=lambda: controller.show_frame(ComputingPage), width=20)
        balance_button.place(relx=.75, rely=.2, anchor= CENTER)   