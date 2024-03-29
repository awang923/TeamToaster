from fileinput import filename
import tkinter as tk
from tkinter import *
import globals
from app import *
from datetime import datetime
import re
from operation import Operation
import upload_manifest_page
#from frontend.app import Node, search

class ComputingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #load_prompt = Label(self, text = "Computing...")
        #load_prompt.place(relx=.5, rely=.1, anchor= CENTER)

        ship_name = Label(self)
        ship_name.place(relx =.05, rely =.1, anchor = NW)

        def ship_name_click():
            if globals.string_filename == "":
                print("EMPTY")
            else:
                print(globals.string_filename)
            ship_name.config(text=globals.string_filename)

        ship_name_button = Button(self, text = "SHOW CURRENT SHIP NAME", command=lambda: ship_name_click())
        ship_name_button.place(relx =.05, rely =.05, anchor = NW)

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

        
        compute_time_label = Label(self, text = "")
        compute_time_label.place(relx=.5, rely=.1, anchor=CENTER)
        
        moves_time = Label(self, text ="")
        moves_time.place(relx = .5, rely = 0.9, anchor=CENTER)

        moves_listbox = Listbox(self)
        moves_listbox.place(relx = .5, rely =.3, anchor=CENTER)

        done_button = Button(self, text="DONE")
        done_button.place(rely=.95, relx=.9, anchor=SE)

        already_done = Label(self, text = "")
        already_done.place(relx = .5, rely =.5, anchor=CENTER)

        def on_done_press():
            print("TEST")
            moves_listbox.delete(0, END)
            compute_time_label.config(text="")
            moves_time.config(text="")
            print(globals.operations_list)
            controller.show_frame(Operation)

        def open_reminder():
                popup = Toplevel(self)
                popup.geometry("750x250")
                popup_label = Label(
                    popup, text="Operation done.\n Outbound manifest written to desktop. \n to mail the updated Manifest.")
                popup_label.place(relx=.5, rely=.4, anchor=CENTER)
                confirm_button = Button(
                    popup, text="Confirm", command=lambda: on_confirm_click(popup))
                confirm_button.place(relx=.5, rely=.6, anchor=CENTER)

        def on_confirm_click(top):
            top.destroy()
            top.update()
            globals.init()
            # for widget in ship_frame.winfo_children():
            #     widget.destroy()
            #self.order_index = 0
            #self.order_label_y = 0.1
            #self.prev_label = None
            #for widget in animation_frame.winfo_children():
                #widget.destroy()
            controller.show_frame(upload_manifest_page.UploadManifestPage)

        def compute():
            step_y = 0.2
            print(globals.op)

            if globals.op == 'transfer':
                if len(globals.unload_list) != 0:
                    print("UNLOADING ONLY")
                    root = Node(globals.ship, buffer_init, globals.unload_list, 'transfer')
                    initial_time = time.time()
                    goal = search(root)
                    unload_buffer_node = unload_buffer(goal)
                    load_ship_node = load_ship(unload_buffer_node, globals.load_list)
                    update_manifest(load_ship_node.state, globals.string_filename)
                    #print(load_ship_node.state)
                    compute_time = (time.time() - initial_time) * 1000
                    compute_time_label.config(text = "Total Time Computing = " + str(compute_time) + "ms")
                    #compute_time_label.place(relx=.5, rely=.1, anchor=CENTER)
                    for i in order_of_operations(load_ship_node):
                        moves_listbox.insert(END, i + "\n")
                        #step = Label(self, text=i)
                        #step.place(relx = .5, rely = step_y, anchor=CENTER)
                        #step_y += 0.05
                        #print(i)
                    moves_time.config(text = "Estimated Time to Perform Moves = " + str(load_ship_node.g) +"min")
                    #moves_time.place(relx = .5, rely = 0.9, anchor=CENTER)
                    globals.operations_list = order_of_operations(load_ship_node)
                    done_button.config(command=lambda: on_done_press())
                else:
                    initial_time = time.time()
                    root = Node(globals.ship, buffer_init, globals.unload_list, 'transfer')
                    load_ship_node = load_ship(root, globals.load_list)
                    compute_time = (time.time() - initial_time) * 1000
                    compute_time_label.config(text = "Total Time Computing = " + str(compute_time) + "ms")
                    #compute_time_label.place(relx=.5, rely=.1, anchor=CENTER)
                    for i in order_of_operations(load_ship_node):
                        moves_listbox.insert(END, i + "\n")
                        #step = Label(self, text=i)
                        #step.place(relx = .5, rely = step_y, anchor=CENTER)
                        #step_y += 0.05
                        #print(i)
                    moves_time.config(text = "Estimated Time to Perform Moves = " + str(load_ship_node.g) +"min")
                    #moves_time.place(relx = .5, rely = step_y, anchor=CENTER)
                    globals.operations_list = order_of_operations(load_ship_node)
                    done_button.config(command=lambda: on_done_press())
            elif globals.op == 'balance':
                root = Node(globals.ship, buffer_init, globals.unload_list, 'balance')
                initial_time = time.time()
                goal = search(root)
                if goal:
                    unload_buffer_node = unload_buffer(goal)
                    compute_time = (time.time() - initial_time) * 1000
                    compute_time_label.config(text = "Total Time Computing = " + str(compute_time) + "ms")
                    #compute_time_label.place(relx=.5, rely=.1, anchor=CENTER)
                    for i in order_of_operations(unload_buffer_node):
                        moves_listbox.insert(END, i + "\n")
                        #step = Label(self, text=i)
                        #step.place(relx = .5, rely = step_y, anchor=CENTER)
                        #step_y += 0.05
                        #print(i)
                    moves_time.config(text = "Estimated Time to Perform Moves = " + str(unload_buffer_node.g) +"min")
                    #moves_time.place(relx = .5, rely = step_y, anchor=CENTER)
                    globals.operations_list = order_of_operations(unload_buffer_node)
                    done_button.config(command=lambda: on_done_press())
                else:
                    already_done.config(text="ALREADY BALANCED, NO MOVES TO BE MADE")
                    done_button.config(command=lambda: open_reminder())
                    update_manifest(globals.ship, globals.string_filename)
                    

            
        



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
