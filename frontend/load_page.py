import tkinter as tk
from tkinter import *
from unload_page import InputUnloadPage

class InputLoadPage(tk.Frame):
    y = 0.2
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        load_prompt = Label(self, text = "Please input all containers to be loaded")
        load_prompt.place(relx=.5, rely=.1, anchor= CENTER)

        container_name_entry = Entry(self)
        container_name_entry.place(relx=.25, rely=.2, anchor= CENTER)
        container_name_entry.insert(0, 'Enter Container Name')
        container_name_entry.configure(state='disabled')
        container_name_entry.bind('<Button-1>', lambda x: on_focus_in(container_name_entry))
        container_name_entry.bind('<FocusOut>', lambda x: on_focus_out(container_name_entry, 'Enter Container Name'))        
        container_weight_entry = Entry(self)
        container_weight_entry.place(relx=.75, rely=.2, anchor= CENTER)
        container_weight_entry.insert(0, 'Enter Container Weight')
        container_weight_entry.configure(state='disabled')
        container_weight_entry.bind('<Button-1>', lambda x: on_focus_in(container_weight_entry))
        container_weight_entry.bind('<FocusOut>', lambda x: on_focus_out(container_weight_entry, 'Enter Container Weight'))

        def on_focus_in(entry):
            if entry.cget('state') == 'disabled':
                entry.configure(state='normal')
                entry.delete(0,'end')

        def on_focus_out(entry, placeholder):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.configure(state='disabled')

        def onKeyPress(event):
            self.y += 0.05
            container_name_entry = Entry(self)
            container_name_entry.place(relx=.25, rely=self.y, anchor= CENTER)
            container_name_entry.insert(0, 'Enter Container Name')
            container_name_entry.configure(state='disabled')
            container_name_entry.bind('<Button-1>', lambda x: on_focus_in(container_name_entry))
            container_name_entry.bind('<FocusOut>', lambda x: on_focus_out(container_name_entry, 'Enter Container Name'))        
            container_weight_entry = Entry(self)
            container_weight_entry.place(relx=.75, rely=self.y, anchor= CENTER)
            container_weight_entry.insert(0, 'Enter Container Weight')
            container_weight_entry.configure(state='disabled')
            container_weight_entry.bind('<Button-1>', lambda x: on_focus_in(container_weight_entry))
            container_weight_entry.bind('<FocusOut>', lambda x: on_focus_out(container_weight_entry, 'Enter Container Weight'))

        controller.bind('<Return>', onKeyPress)

        done_button = Button(self, text="DONE", command=lambda: controller.show_frame(InputUnloadPage))
        done_button.place(rely=.9, relx=.9, anchor=SE)

