from cmath import e
from fileinput import filename
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from select_op_page import SelectOperationPage
from app import *
import globals
from datetime import datetime


class UploadManifestPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        upload_prompt = Label(self, text="Please upload the manifest")
        upload_prompt.place(relx=.5, rely=.1, anchor=CENTER)

        comment_box = Entry(self, width=50)
        comment_box.place(relx=.1, rely=.95, anchor=W)
        comment_box.bind('<Button-1>', lambda x: comment_focus_in(comment_box))
        comment_box.bind('<FocusOut>', lambda x: comment_focus_out(
            comment_box, "Enter comment here"))

        def sign_in_popup():
            popup = Toplevel(self)
            popup.geometry("700x250")
            popup.title("Sign In")
            #popup_label = Label(popup, text = "SIGN IN POPUP")
            # popup_label.pack(pady=10)
            username_input = Entry(popup, width=20)
            username_input.bind(
                '<Button-1>', lambda x: on_focus_in(username_input))
            username_input.bind('<FocusOut>', lambda x: on_focus_out(
                username_input, 'First Last'))
            username_input.place(relx=.5, rely=.15, anchor=CENTER)
            error_msg = Label(popup, text="")
            error_msg.place(relx=.5, rely=.3, anchor=CENTER)

            def open_error_popup():
                error_msg.config(text="Enter your first name and last name")

            def sign_in_on_click():
                # print(username_input.get())
                if(username_input.get() != "" and username_input.get() != "First Last"):
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("frontend/logfile.txt", 'a') as logfile:
                        logfile.write(
                            current_time + " " + username_input.get() + " signed in." + "\n")
                    logfile.close()
                    popup.destroy()
                    # controller.show_frame(UploadManifestPage)
                else:
                    #print("ERROR MESSAGE")
                    open_error_popup()
            popup_sign_in_button = Button(
                popup, text="Sign In", command=lambda: sign_in_on_click(), width=20)
            popup_sign_in_button.place(relx=.5, rely=.5, anchor=CENTER)

            def on_focus_in(entry):
                if entry.cget('state') == 'disabled':
                    entry.configure(state='normal')
                    entry.delete(0, 'end')
                    error_msg['text'] = ""

            def on_focus_out(entry, placeholder):
                if entry.get() == '':
                    entry.insert(0, placeholder)
                    entry.configure(state='disabled')

        sign_in_button = Button(self, text="Sign In",
                                command=lambda: sign_in_popup())
        sign_in_button.place(relx=.8, rely=.1, anchor="e")

        def open_file():
            # global file
            global filename
            filename = filedialog.askopenfilename(
                title="Select File", filetypes=(("txt file", "*.txt"),))
            filename_label = Label(self, text=filename)
            filename_label.place(relx=.5, rely=.3, anchor=CENTER)

        def on_done_pressed():
            # print(filename)
            globals.string_filename = str(filename)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("frontend/logfile.txt", 'a') as logfile:
                logfile.write(
                    current_time + " " + globals.string_filename + " has been opened." + "\n")
            logfile.close()
            print(globals.string_filename +
                  "string_filename upload_manifest_page")
            parse_manifest(globals.ship, globals.string_filename)
            print(globals.ship)
            controller.show_frame(SelectOperationPage)

        upload_button = Button(self, text="Select File", command=open_file)
        upload_button.place(relx=.5, rely=.2, anchor=CENTER)

        def comment_click():
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("frontend/logfile.txt", 'a') as logfile:
                logfile.write(current_time + " " + comment_box.get() + "\n")
            logfile.close()
            comment_box.delete(0, 'end')

        comment_button = Button(self, text="Comment",
                                command=lambda: comment_click())
        comment_button.place(relx=.7, rely=.95, anchor=E)

        def comment_focus_in(entry):
            if entry.cget('state') == 'disabled':
                entry.configure(state='normal')
                entry.delete(0, 'end')

        def comment_focus_out(entry, placeholder):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.configure(state='disabled')

        done_button = Button(
            self, text="DONE", command=lambda: on_done_pressed())
        done_button.place(rely=.95, relx=.9, anchor=SE)
