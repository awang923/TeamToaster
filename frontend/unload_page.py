import tkinter as tk
from tkinter import *
from computing_page import ComputingPage

class InputUnloadPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        unload_prompt = Label(self, text = "Please input all containers to be unloaded")
        unload_prompt.place(relx=.5, rely=.1, anchor= CENTER)

        table_frame = Frame(self)
        table_frame.place(relx=.5, rely=.5, anchor=CENTER)

        for x in range(12):
            for y in range(8):
                b = Button(table_frame, text=f'{y+1}, {12-x}', height=3, width=5)
                b.grid(row=x,column=y)
        
        done_button = Button(self, text="DONE", command=lambda: controller.show_frame(ComputingPage))
        done_button.place(rely=.9, relx=.9, anchor=SE)
