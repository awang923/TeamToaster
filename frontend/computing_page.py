import tkinter as tk
from tkinter import *

class ComputingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        load_prompt = Label(self, text = "Please input all containers to be loaded")
        load_prompt.place(relx=.5, rely=.1, anchor= CENTER)