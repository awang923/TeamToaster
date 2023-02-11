import tkinter as tk
from tkinter import *
from upload_manifest_page import UploadManifestPage
from unload_page import InputUnloadPage

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        intro_prompt = Label(self, text = "Welcome to Team Toaster's Application")
        intro_prompt.place(relx=.5, rely=.1, anchor= CENTER)
        # intro_prompt.grid(row = 0, pady=10, padx = 100)

        username_input = Entry(self, width=20)
        username_input.insert(0, 'First Last')
        username_input.configure(state='disabled')
        username_input.bind('<Button-1>', lambda x: on_focus_in(username_input))
        username_input.bind('<FocusOut>', lambda x: on_focus_out(username_input, 'First Last'))
        username_input.place(relx=.5, rely=.15, anchor= CENTER)
        
        # def show_signin_button():
        sign_in_button = Button(self, text="Sign In", command=lambda: controller.show_frame(UploadManifestPage) if username_input.get() !='' else open_error_popup(), width=20)
        sign_in_button.place(relx=.5, rely=.25, anchor= CENTER)


        test_button = Button(self, text="test", command=lambda: controller.show_frame(InputUnloadPage))
        test_button.place(relx=.5, rely=.3, anchor=CENTER)
        
        # def onclick_sign_in():
        #     sign_in_msg = Label(root, text="Hello " + username_input.get(), fg='black')
        #     sign_in_msg.pack()
        def open_error_popup():
            error_msg = Label(self, text="Enter your first name and last name")
            error_msg.place(relx=.5, rely=.2, anchor= CENTER)

        # if username_input.get() !='':
        #     show_signin_button()
        # else:
        #     open_error_popup()

        def on_focus_in(entry):
            if entry.cget('state') == 'disabled':
                entry.configure(state='normal')
                entry.delete(0,'end')

        def on_focus_out(entry, placeholder):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.configure(state='disabled')
