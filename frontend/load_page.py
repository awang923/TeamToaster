import tkinter as tk
from tkinter import *
from unload_page import InputUnloadPage
import globals
from datetime import datetime


class InputLoadPage(tk.Frame):
    count = 0
    y = 0.2

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        load_prompt = Label(
            self, text="Please input all containers to be loaded")
        load_prompt.place(relx=.5, rely=.1, anchor=CENTER)
        instructions = Label(
            self, text="Press enter after entering containers to input")
        instructions.place(relx=.5, rely=.2, anchor=CENTER)

        comment_box = Entry(self, width=50)
        comment_box.place(relx=.1, rely=.95, anchor=W)
        comment_box.bind('<Button-1>', lambda x: comment_focus_in(comment_box))
        comment_box.bind('<FocusOut>', lambda x: comment_focus_out(
            comment_box, "Enter comment here"))

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

        container_name_entry = Entry(self)
        container_name_entry.place(relx=.25, rely=.3, anchor=CENTER)
        container_name_entry.insert(0, 'Enter Container Name')
        container_name_entry.configure(state='disabled')
        container_name_entry.bind(
            '<Button-1>', lambda x: on_focus_in(container_name_entry))
        container_name_entry.bind('<FocusOut>', lambda x: on_focus_out(
            container_name_entry, 'Enter Container Name'))
        container_weight_entry = Entry(self)
        container_weight_entry.place(relx=.75, rely=.3, anchor=CENTER)
        container_weight_entry.insert(0, 'Enter Container Weight (kg)')
        container_weight_entry.configure(state='disabled')
        container_weight_entry.bind(
            '<Button-1>', lambda x: on_focus_in(container_weight_entry))
        container_weight_entry.bind('<FocusOut>', lambda x: on_focus_out(
            container_weight_entry, 'Enter Container Weight'))
        #load_list.append((lambda: container_weight_entry.get(), lambda: container_name_entry.get()))
        error_message = Label(self, text="")
        error_message.place(relx=.75, rely=.4, anchor=CENTER)
        confirm_enter = Label(self, text="")
        confirm_enter.place(relx=.5, rely=.5, anchor=CENTER)

        def error_fade():
            error_message['text'] = ""

        def confirm_fade():
            confirm_enter['text'] = ""

        def on_focus_in(entry):
            if entry.cget('state') == 'disabled':
                entry.configure(state='normal')
                entry.delete(0, 'end')
                error_fade()
                #load_list.append((container_weight_entry.get(), container_name_entry.get()))

        def on_focus_out(entry, placeholder):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.configure(state='disabled')

        def onKeyPress(event):
            #self.y += 0.05
            # container_name_entry = Entry(self)
            # container_name_entry.place(relx=.25, rely=self.y, anchor= CENTER)
            # container_name_entry.insert(0, 'Enter Container Name')
            # container_name_entry.configure(state='disabled')
            # container_name_entry.bind('<Button-1>', lambda x: on_focus_in(container_name_entry))
            # container_name_entry.bind('<FocusOut>', lambda x: on_focus_out(container_name_entry, 'Enter Container Name'))
            # container_weight_entry = Entry(self)
            # container_weight_entry.place(relx=.75, rely=self.y, anchor= CENTER)
            # container_weight_entry.insert(0, 'Enter Container Weight')
            # container_weight_entry.configure(state='disabled')
            # container_weight_entry.bind('<Button-1>', lambda x: on_focus_in(container_weight_entry))
            # container_weight_entry.bind('<FocusOut>', lambda x: on_focus_out(container_weight_entry, 'Enter Container Weight'))
            try:
                int(container_weight_entry.get())
                globals.load_list.append(
                    (int(container_weight_entry.get()), container_name_entry.get()))
                confirm_enter.config(text=container_name_entry.get(
                ) + ", " + container_weight_entry.get() + "kg has been entered")
                #confirm_enter.after(5000, confirm_fade())
                container_name_entry.delete(0, END)
                container_weight_entry.delete(0, END)
            except ValueError:
                error_message.config(text="Only integers allowed for weight!")
                #error_message.after(5000, error_fade())
                container_weight_entry.delete(0, END)

        controller.bind('<Return>', onKeyPress)

        def on_done_pressed():
            for x in globals.load_list:
                print(x)
            print(globals.string_filename + "string_filename load_page")
            controller.show_frame(InputUnloadPage)

        done_button = Button(
            self, text="DONE", command=lambda: on_done_pressed())
        done_button.place(rely=.9, relx=.9, anchor=SE)

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
