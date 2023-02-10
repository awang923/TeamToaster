import tkinter as tk
from tkinter import *

class InputUnloadPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        unload_prompt = Label(self, text = "Please input all containers to be unloaded")
        unload_prompt.place(relx=.5, rely=.1, anchor= CENTER)