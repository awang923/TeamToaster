from cgitb import text
import tkinter as tk
from tkinter import *
#from tkinter import tix
from tkinter.tix import *
from tkinter import ttk
from turtle import bgcolor, onclick, width
from computing_page import ComputingPage
import re
#from tktooltip import ToolTip

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

        #parent.config(width=3000)

        unload_prompt = Label(self, text = "Please input all containers to be unloaded")
        unload_prompt.place(relx=.5, rely=.1, anchor= CENTER)

        table_frame = Frame(self)
        table_frame.place(relx=.5, rely=.5, anchor=CENTER)

        manifest = open('TeamToaster/files/manifest.txt', 'r')
        manifest_lines = manifest.readlines()

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

        tooltipString = ""

        def on_click(container_name, mass, x_coord, y_coord):
            print("["+ x_coord+ ", " +  y_coord + "] " + container_name + ", "+ mass)
        temp = 0
        for x in range(8,0,-1):
            temp += 1
            for y in range(12):
                for line in manifest_lines:
                    regex_matches = re.search(regex, str(line))
                    #print(tooltipString)
                    if (regex_matches.group(1).lstrip('0') == str(temp) and regex_matches.group(2).lstrip('0') == str(y+1)):
                        if regex_matches.group(4) == "NAN":
                            b = Button(table_frame, text=regex_matches.group(4), height=3, width=6, highlightbackground='#CEBBBB')
                            tooltipString = b.cget('text')
                        elif regex_matches.group(4) == "UNUSED":
                            b = Button(table_frame, text=regex_matches.group(4), height=3, width=6, highlightbackground='white')
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

        
        done_button = Button(self, text="DONE", command=lambda: controller.show_frame(ComputingPage))
        done_button.place(rely=.9, relx=.9, anchor=SE)
    
