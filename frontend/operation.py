import tkinter as tk
from tkinter import *
import re
from app import *
import globals

class Operation(tk.Frame):
    #order_left = len(globals.operations_list)
    order_index = 0
    order_label_y = 0.1
    prev_label = None
   
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #manifest = open(globals.string_filename, 'r')
        #manifest_lines = manifest.readlines()
        #regex = ".(\d\d),(\d\d).,\s{(\d*)}.\s([a-zA-Z]*)"

        #order_label = Label(self, text=globals.operations_list[self.order_index], fg='red')
        #order_label.place(relx=0.2, rely=self.order_label_y, anchor=CENTER)
        #self.order_label_y = self.order_label_y + 0.03
        #self.order_index = self.order_index + 1

        def on_view_click():
            on_view_click.order_left = len(globals.operations_list)
            manifest = open(globals.string_filename, 'r')
            manifest_lines = manifest.readlines()
            regex = ".(\d\d),(\d\d).,\s{(\d*)}.\s([a-zA-Z]*)"

            order_label = Label(self, text=globals.operations_list[self.order_index], fg='red')
            order_label.place(relx=0.2, rely=self.order_label_y, anchor=CENTER)
            self.order_label_y = self.order_label_y + 0.03
            self.order_index = self.order_index + 1
        
            def add_order():
                temp = Label(self, text=globals.operations_list[self.order_index], fg='red')
                return temp

            order_regex = ".\s([a-zA-Z]*[(\d\d),(\d\d)])"
            def parse_order(order):
                order_matches = re.search(order_regex, globals.operations_list[self.order_index])
                

            ship_frame = Frame(self)
            temp = 9
            containers = []
            for x in range(8):
                temp -= 1
                containers.append([])
                for y in range(12):
                    for line in manifest_lines:
                        regex_matches = re.search(regex, str(line))
                        if (regex_matches.group(1).lstrip('0') == str(temp) and regex_matches.group(2).lstrip('0') == str(y+1)):
                            if regex_matches.group(4) == "NAN":
                                box = LabelFrame(ship_frame, width=40, height=40, bg='#CEBBBB')
                                l = Label(box)
                                l.place(relx=0.5, rely=0.5, anchor=CENTER)
                            elif regex_matches.group(4) == "UNUSED":
                                box = LabelFrame(ship_frame, width=40, height=40)
                                l = Label(box)
                                l.place(relx=0.5, rely=0.5, anchor=CENTER)
                            else:
                                box = LabelFrame(ship_frame, width=40, height=40)
                                l = Label(box, text=regex_matches.group(4)[:6])
                                l.place(relx=0.5, rely=0.5, anchor=CENTER)
                            containers[x].append(l)                            
                    box.grid(row=x, column=y)
            ship_frame.place(relx=0.74, rely=0.45, anchor=CENTER)
            # print(containers[7][1].cget('text'))
            # print(l.cget('text'))

            #create the ui of ship & buffer
            buffer_frame = Frame(self)
            for x in range(4):
                for y in range(24):
                    box = LabelFrame(buffer_frame, width=40, height= 40)
                    l = Label(box)
                    l.place(relx=0.5, rely=0.5, anchor=CENTER)
                    box.grid(row=x, column=y)
            buffer_frame.place(relx=0.5, rely=0.78, anchor=CENTER)
            
            def on_next_press():
                if on_view_click.order_left > 1:
                    order_label['fg'] = 'black'
                    if self.prev_label is not None:
                        self.prev_label['fg'] = 'black'
                    curr_label = add_order()
                    curr_label.place(relx=0.2, rely=self.order_label_y, anchor=CENTER)
                    self.order_label_y = self.order_label_y + 0.03
                    self.order_index = self.order_index + 1
                    self.prev_label = curr_label
                    
                on_view_click.order_left = on_view_click.order_left-1

            done_button = Button(self, text="NEXT", command=lambda: on_next_press())
            done_button.place(rely=.95, relx=.9, anchor=SE)

        view_animation = Button(self, text = "View Animation", command= lambda:on_view_click())
        view_animation.place(relx=.5, rely=.05, anchor= CENTER)
    

       