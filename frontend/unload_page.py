from cgitb import text
from fileinput import filename
from importlib.metadata import files
import tkinter as tk
from tkinter import *
#from tkinter import tix
from tkinter.tix import *
from tkinter import ttk
from turtle import bgcolor, onclick, width
from computing_page import ComputingPage
import re
#from tktooltip import ToolTip
import globals
from datetime import datetime

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"), fg="black")
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

class InputUnloadPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

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

        #print(string_filename)

        #parent.config(width=3000)

        unload_prompt = Label(self, text = "Please input all containers to be unloaded")
        unload_prompt.place(relx=.5, rely=.1, anchor= CENTER)


        table_frame = Frame(self)
        table_frame.place(relx=.5, rely=.5, anchor=CENTER)

        #print(globals.string_filename + "string_filename unload_page")
        #manifest_unload = open("frontend/manifest.txt", 'r')
        #manifest_lines = manifest_unload.readlines()
        #manifest_lines = []
        #if globals.string_filename != "":
            #manifest_unload = open(globals.string_filename, 'r')
            #manifest_lines = manifest_unload.readlines()


        regex = ".(\d\d),(\d\d).,\s{(\d*)}.\s([a-zA-Z]*)"

        #for x in range(12):
            #for y in range(8):
                #b = Button(table_frame, text=f'{y+1}, {12-x}', height=3, width=5)
                #b.grid(row=x,column=y)

        #for line in manifest_lines:
            #regex_matches = re.search(regex, line)
            #print(regex_matches.group(1).lstrip('0'))
            #print(regex_matches.group(2).lstrip('0'))
            #print(regex_matches.group(4))
            #print("\n")
        
        #status_label = Label(self, text='', bd=1, relief=SUNKEN, anchor=E)
        #status_label.pack(fill=X, side=BOTTOM, ipady=2)

        #def button_hover(e):
            #status_label.config(text=b.cget('text'))

        #def button_hover_leave(e):
            #status_label.config(text=' ')

        #tooltipString = ""
        confirm_unload = Label(self, text="")
        confirm_unload.place(relx = .5, rely=.85, anchor=CENTER)

        def on_click(container_name, mass, x_coord, y_coord):
            print("["+ x_coord+ ", " +  y_coord + "] " + container_name + ", "+ mass)
            confirm_unload.config(text= container_name + ", " + mass +"kg has been entered")
            globals.unload_list.append((int(mass), container_name))
        
        def view_grid_click():
            tooltipString = ""
            print(globals.string_filename + "string_filename unload_page")
            manifest_unload = open(globals.string_filename, 'r')
            manifest_lines = manifest_unload.readlines()
            temp = 0
            for x in range(8,0,-1):
                temp += 1
                for y in range(12):
                    for line in manifest_lines:
                        regex_matches = re.search(regex, str(line))
                        #print(tooltipString)
                        if (regex_matches.group(1).lstrip('0') == str(temp) and regex_matches.group(2).lstrip('0') == str(y+1)):
                            if regex_matches.group(4) == "NAN":
                                b = Button(table_frame, text=regex_matches.group(4), height=3, width=6, highlightbackground='#CEBBBB', state="disabled")
                                tooltipString = b.cget('text')
                            elif regex_matches.group(4) == "UNUSED":
                                b = Button(table_frame, text=regex_matches.group(4), height=3, width=6, highlightbackground='white', state="disabled")
                                tooltipString = b.cget('text')
                            else:
                                container_name = regex_matches.group(4)
                                mass=regex_matches.group(3)
                                x_coord = regex_matches.group(1)
                                y_coord = regex_matches.group(2)
                                b = Button(table_frame, text=regex_matches.group(4)[:6], height=3, width=6, highlightbackground='#8FFF3A', 
                                        command= lambda container_name=container_name, mass=mass, x_coord=x_coord, y_coord=y_coord: 
                                        on_click(container_name,mass,x_coord,y_coord))
                                tooltipString = container_name + ", " + mass + "kg"
                                
                            #b = Button(table_frame, text=regex_matches.group(4), height=3, width=5)
                            #print(regex_matches.group(4))
                            b.grid(row=x,column=y)
                            CreateToolTip(b, tooltipString)

        view_grid = Button(self, text="VIEW GRID", command=lambda: view_grid_click())
        view_grid.place(relx=.5, rely=.15, anchor= CENTER)
        
        def done_button_click():
            for x in globals.unload_list:
                print(x)
            controller.show_frame(ComputingPage)

        
        done_button = Button(self, text="DONE", command=lambda: done_button_click())
        done_button.place(rely=.9, relx=.9, anchor=SE)

        def clear_press():
            globals.load_list.clear()
            confirm_unload.config(text="LOAD LIST HAS BEEN CLEARED")
            print(globals.load_list)
        
        clear_button = Button(self, text="CLEAR LOAD LIST", command=lambda: clear_press(), width=15)
        clear_button.place(rely=.85, relx=.9, anchor=SE)

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
        sign_in_button.place(relx=.8, rely=.1, anchor="e")
    
