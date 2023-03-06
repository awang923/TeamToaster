from fileinput import filename
import tkinter as tk
from tkinter import *
import globals
from app import *
from datetime import datetime
import re

#from frontend.app import Node, search

class ComputingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #load_prompt = Label(self, text = "Computing...")
        #load_prompt.place(relx=.5, rely=.1, anchor= CENTER)

        comment_box = Entry(self, width = 50)
        comment_box.place(relx=.1, rely =.95, anchor=W)
        comment_box.bind('<Button-1>', lambda x: comment_focus_in(comment_box))
        comment_box.bind('<FocusOut>', lambda x: comment_focus_out(comment_box, "Enter comment here"))

        def comment_click():
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("frontend/logfile.txt", 'a') as logfile:
                logfile.write(current_time + " " + comment_box.get() + "\n")
            logfile.close()
            comment_box.delete(0, 'end')

        comment_button = Button(self, text = "Comment", command= lambda: comment_click())
        comment_button.place(relx = .7, rely = .95, anchor=E)

        def comment_focus_in(entry):
            if entry.cget('state') == 'disabled':
                    entry.configure(state='normal')
                    entry.delete(0,'end')
        
        def comment_focus_out(entry, placeholder):
            if entry.get() == '':
                    entry.insert(0, placeholder)
                    entry.configure(state='disabled')

        buffer_init = {}
        for r in range(4):
            for c in range(24):
                buffer_init[(r + 1, c + 1)] = [0, 'UNUSED']

        
        def compute():
            step_y = 0.2
            print(globals.op)

            if globals.op == 'transfer':
                root = Node(globals.ship, buffer_init, globals.unload_list, 'transfer')
                initial_time = time.time()
                goal = search(root)
                unload_buffer_node = unload_buffer(goal)
                load_ship_node = load_ship(unload_buffer_node, globals.load_list)
                #print(load_ship_node.state)
                compute_time = (time.time() - initial_time) * 1000
                compute_time_label = Label(self, text = "Total Time Computing = " + str(compute_time) + "ms")
                compute_time_label.place(relx=.5, rely=.1, anchor=CENTER)
                for i in order_of_operations(load_ship_node):
                    step = Label(self, text=i)
                    step.place(relx = .5, rely = step_y, anchor=CENTER)
                    step_y += 0.05
                    #print(i)
                moves_time = Label(self, text = "Estimated Time to Perform Moves = " + str(load_ship_node.g) +"min")
                moves_time.place(relx = .5, rely = step_y, anchor=CENTER)
            elif globals.op == 'balance':
                root = Node(globals.ship, buffer_init, globals.unload_list, 'balance')
                initial_time = time.time()
                goal = search(root)
                unload_buffer_node = unload_buffer(goal)
                compute_time = (time.time() - initial_time) * 1000
                compute_time_label = Label(self, text = "Total Time Computing = " + str(compute_time) + "ms")
                compute_time_label.place(relx=.5, rely=.1, anchor=CENTER)
                for i in order_of_operations(unload_buffer_node):
                    step = Label(self, text=i)
                    step.place(relx = .5, rely = step_y, anchor=CENTER)
                    step_y += 0.05
                    #print(i)
                moves_time = Label(self, text = "Estimated Time to Perform Moves = " + str(unload_buffer_node.g) +"min")
                moves_time.place(relx = .5, rely = step_y, anchor=CENTER)



        #ship_name_regex = "(.*)\.txt"
        #test_string = globals.get_filename()
        #print("test_string: " + globals.get_filename())
        #ship_name_matches = re.search(ship_name_regex, str(test_string))
        #ship_label = Label(self, text = "Ship: " + ship_name_matches.group(1))
        #ship_label.place(relx=.1, rely=.05, anchor=CENTER)
       
        compute_button = Button(self, text = "COMPUTE STEPS", command= lambda:compute())
        compute_button.place(relx=.5, rely=.05, anchor= CENTER)

        def sign_in_popup():
            popup = Toplevel(self)
            popup.geometry("700x250")
            popup.title("Sign In")
            #popup_label = Label(popup, text = "SIGN IN POPUP")
            #popup_label.pack(pady=10)
            username_input = Entry(popup, width=20)
            username_input.bind('<Button-1>', lambda x: on_focus_in(username_input))
            username_input.bind('<FocusOut>', lambda x: on_focus_out(username_input, 'First Last'))
            username_input.place(relx=.5, rely=.15, anchor= CENTER)
            error_msg = Label(popup, text ="")
            error_msg.place(relx=.5, rely=.3, anchor= CENTER)
        
            def open_error_popup():
                error_msg.config(text="Enter your first name and last name")

            def sign_in_on_click():
                #print(username_input.get())
                if(username_input.get() != "" and username_input.get() != "First Last"):
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("frontend/logfile.txt", 'a') as logfile:
                        logfile.write(current_time + " " + username_input.get() + " signed in." + "\n")
                    logfile.close()
                    popup.destroy()
                    #controller.show_frame(UploadManifestPage)
                else:
                    #print("ERROR MESSAGE")
                    open_error_popup()
            popup_sign_in_button = Button(popup, text="Sign In", command=lambda: sign_in_on_click(), width=20)
            popup_sign_in_button.place(relx=.5, rely=.5, anchor= CENTER)

            def on_focus_in(entry):
                if entry.cget('state') == 'disabled':
                    entry.configure(state='normal')
                    entry.delete(0,'end')
                    error_msg['text'] = ""

            def on_focus_out(entry, placeholder):
                if entry.get() == '':
                    entry.insert(0, placeholder)
                    entry.configure(state='disabled')

        sign_in_button = Button(self, text = "Sign In", command= lambda: sign_in_popup())
        sign_in_button.place(relx=.8, rely=.05, anchor="e")