import tkinter as tk
from tkinter import *
import re
from app import *
import globals
import time
import upload_manifest_page


class Operation(tk.Frame):
    #order_left = len(globals.operations_list)
    order_index = 0
    order_label_y = 0.1
    prev_label = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

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
                    with open("TeamToaster/frontend/logfile.txt", 'a') as logfile:
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

        #manifest = open(globals.string_filename, 'r')
        #manifest_lines = manifest.readlines()
        #regex = ".(\d\d),(\d\d).,\s{(\d*)}.\s([a-zA-Z]*)"

        #order_label = Label(self, text=globals.operations_list[self.order_index], fg='red')
        #order_label.place(relx=0.2, rely=self.order_label_y, anchor=CENTER)
        #self.order_label_y = self.order_label_y + 0.03
        #self.order_index = self.order_index + 1

        def on_view_click():
            # on_view_click.order_left = len(globals.operations_list)
            # manifest = open(globals.string_filename, 'r')
            on_view_click.order_left = len(orders)
            manifest = open('TeamToaster/files/manifest.txt', 'r')
            manifest_lines = manifest.readlines()
            regex = ".(\d\d),(\d\d).,\s{(\d*)}.\s([a-zA-Z]*)"

            # parses operation string for movement location and coordinates
            def parse_string(str):
                text = str.split()

                # type of operation (move, load, unload)
                operation = text[0]

                # locations of movement
                prev, dest = None, None

                # get containers original location
                if operation == 'Move':
                    # move from buffer to ship
                    if text[1] == 'BUFFER':
                        prev_coords = text[2]
                        dest_coords = text[-1]
                        prev_loc = 'BUFFER'
                        dest_loc = 'SHIP'
                    else:
                        # move from ship to buffer
                        if text[-2] == 'BUFFER':
                            prev_coords = text[1]
                            dest_coords = text[-1]
                            prev_loc = 'SHIP'
                            dest_loc = 'BUFFER'
                        # move from ship to ship
                        else:
                            prev_coords = text[1]
                            dest_coords = text[-1]
                            prev_loc = 'SHIP'
                            dest_loc = 'SHIP'

                    # get previous location
                    pos = [int(i) for i in prev_coords.strip('][').split(',')]
                    pos = (pos[0], pos[1])
                    prev = (prev_loc, pos)

                    # get destination location
                    pos = [int(i) for i in dest_coords.strip('][').split(',')]
                    pos = (pos[0], pos[1])
                    dest = (dest_loc, pos)

                elif operation == 'Load':
                    pos = [int(i) for i in text[-1].strip('][').split(',')]
                    pos = (pos[0], pos[1])
                    dest = ('SHIP', pos, text[1])
                elif operation == 'Unload':
                    pos = [int(i) for i in text[1].strip('][').split(',')]
                    pos = (pos[0], pos[1])
                    prev = ('SHIP', pos)

                return (prev, dest)

            ship_label = Label(self, text="SHIP")
            ship_label.place(relx=0.53, rely=0.22, anchor=CENTER)
            ship_frame = Frame(self)
            temp = 9
            ship = []
            for x in range(8):
                temp -= 1
                ship.append([])
                for y in range(12):
                    for line in manifest_lines:
                        regex_matches = re.search(regex, str(line))
                        if (regex_matches.group(1).lstrip('0') == str(temp) and regex_matches.group(2).lstrip('0') == str(y+1)):
                            if regex_matches.group(4) == "NAN":
                                box = LabelFrame(
                                    ship_frame, width=40, height=40, bg='#CEBBBB')
                                l = Label(box)
                                l.place(relx=0.5, rely=0.5, anchor=CENTER)
                            elif regex_matches.group(4) == "UNUSED":
                                box = LabelFrame(
                                    ship_frame, width=40, height=40)
                                l = Label(box)
                                l.place(relx=0.5, rely=0.5, anchor=CENTER)
                            else:
                                box = LabelFrame(
                                    ship_frame, width=40, height=40)
                                l = Label(box, text=regex_matches.group(4)[:6])
                                l.place(relx=0.5, rely=0.5, anchor=CENTER)
                            ship[x].append(l)
                    box.grid(row=x, column=y)
            ship_frame.place(relx=0.74, rely=0.45, anchor=CENTER)

            buffer_label = Label(self, text="BUFFER")
            buffer_label.place(relx=0.05, rely=0.65, anchor=CENTER)
            buffer_frame = Frame(self)
            buffer = []
            for x in range(4):
                buffer.append([])
                for y in range(24):
                    box = LabelFrame(buffer_frame, width=40, height=40)
                    l = Label(box)
                    l.place(relx=0.5, rely=0.5, anchor=CENTER)
                    buffer[x].append(l)
                    box.grid(row=x, column=y)
            buffer_frame.place(relx=0.5, rely=0.78, anchor=CENTER)

            truck_label = Label(self, text="TRUCK")
            truck_label.place(relx=0.2, rely=0.5, anchor=CENTER)
            box = LabelFrame(self, width=40, height=40)
            truck_container = Label(box)
            truck_container.place(relx=0.5, rely=0.5, anchor=CENTER)
            box.place(relx=0.2, rely=0.55, anchor=CENTER)

            on_view_click.flag = True
            on_view_click.animate = True

            def update(prev_x, prev_y, dest_x, dest_y, container_name, prev, dest):
                if prev != None and dest != None:
                    if on_view_click.flag:
                        prev[prev_x][prev_y].config(
                            bg='#80BD76', text=container_name)
                        dest[dest_x][dest_y].config(
                            bg=self.cget('bg'), text="")
                        on_view_click.flag = not on_view_click.flag
                    else:
                        prev[dest_x][dest_y].config(
                            bg='#80BD76', text=container_name)
                        dest[prev_x][prev_y].config(
                            bg=self.cget('bg'), text="")
                        on_view_click.flag = not on_view_click.flag
                elif prev == None:
                    if on_view_click.flag:
                        truck_container.config(bg='#80BD76', text=container_name)
                        dest[dest_x][dest_y].config(bg=self.cget('bg'), text="")
                        on_view_click.flag = not on_view_click.flag
                    else:
                        truck_container.config(bg=self.cget('bg'), text="")
                        dest[dest_x][dest_y].config(bg='#80BD76', text=container_name)
                        on_view_click.flag = not on_view_click.flag
                else:
                    if on_view_click.flag:
                        prev[prev_x][prev_y].config(bg='#80BD76', text=container_name)
                        truck_container.config(bg=self.cget('bg'), text="")
                        on_view_click.flag = not on_view_click.flag
                    else:
                        prev[prev_x][prev_y].config(bg=self.cget('bg'), text="")
                        truck_container.config(bg='#80BD76', text=container_name)
                        on_view_click.flag = not on_view_click.flag

            def animation():
                if on_view_click.animate:
                    update(on_view_click.prev_x, on_view_click.prev_y,
                           on_view_click.dest_x, on_view_click.dest_y,
                           on_view_click.container_name,
                           on_view_click.prev, on_view_click.dest)
                    self.after(2000, lambda: animation())

            # order_label = Label(self, text=globals.operations_list[self.order_index], fg='red')
            order_label = Label(self, text=orders[self.order_index], fg='red')
            order_label.place(relx=0.2, rely=self.order_label_y, anchor=CENTER)

            # set x, y, container list and container name for the first animation
            parse_order = parse_string(orders[self.order_index])

            def set_variables(parse_order):
                if parse_order[0] != None:
                    if parse_order[0][0] == 'SHIP':
                        prev = ship
                    elif parse_order[0][0] == 'BUFFER':
                        prev = buffer
                else:
                    prev = None

                if parse_order[1] != None:
                    if parse_order[1][0] == 'SHIP':
                        dest = ship
                    elif parse_order[1][0] == 'BUFFER':
                        dest = buffer
                else:
                    dest = None

                if prev != None:
                    on_view_click.prev_x = (len(prev)-1) - (parse_order[0][1][0]-1)
                    on_view_click.prev_y = parse_order[0][1][1] - 1
                    on_view_click.container_name = prev[on_view_click.prev_x][on_view_click.prev_y].cget('text')
                if dest != None:
                    on_view_click.dest_x = (len(dest)-1) - (parse_order[1][1][0]-1)
                    on_view_click.dest_y = parse_order[1][1][1] - 1
                if prev == None and dest != None:
                    on_view_click.container_name = parse_order[1][2]
                # if prev != None and dest == None:
                #     on_view_click.container_name = prev[on_view_click.prev_x][on_view_click.prev_y].cget('text')

                return prev, dest
            on_view_click.prev, on_view_click.dest = set_variables(parse_order)
            animation()

            def set_end_of_animation():
                #loading
                if on_view_click.prev == None:
                    truck_container.config(bg=self.cget('bg'), text="")
                    on_view_click.dest[on_view_click.dest_x][on_view_click.dest_y].config(bg=self.cget('bg'), text=on_view_click.container_name)
                #unloading
                elif on_view_click.dest == None:
                    on_view_click.prev[on_view_click.prev_x][on_view_click.prev_y].config(bg=self.cget('bg'), text="")
                    truck_container.config(bg=self.cget('bg'), text=on_view_click.container_name)
                else:
                    on_view_click.prev[on_view_click.prev_x][on_view_click.prev_y].config(bg=self.cget('bg'), text="")
                    on_view_click.dest[on_view_click.dest_x][on_view_click.dest_y].config(bg=self.cget('bg'), text=on_view_click.container_name)

            self.order_label_y = self.order_label_y + 0.03
            self.order_index = self.order_index + 1

            def add_order():
                temp = Label(self, text=orders[self.order_index], fg='red')
                return temp

            def on_next_press():
                if on_view_click.order_left > 1:
                    # update animation with new x and y
                    set_end_of_animation()
                    parse_order = parse_string(orders[self.order_index])
                    on_view_click.prev, on_view_click.dest = set_variables(parse_order)
                    animation()

                    # display label with the next order sequence
                    order_label['fg'] = 'black'
                    if self.prev_label is not None:
                        self.prev_label['fg'] = 'black'
                    curr_label = add_order()
                    curr_label.place(
                        relx=0.2, rely=self.order_label_y, anchor=CENTER)
                    self.order_label_y = self.order_label_y + 0.03
                    self.order_index = self.order_index + 1
                    self.prev_label = curr_label
                on_view_click.order_left = on_view_click.order_left-1
                if on_view_click.order_left < 1:
                    set_end_of_animation()
                    on_view_click.animate = False
                    animation()
                    done_button.config(
                        text='DONE', command=lambda: open_reminder())

            done_button = Button(
                self, text="NEXT", command=lambda: on_next_press())
            done_button.place(rely=.95, relx=.9, anchor=SE)

            def open_reminder():
                popup = Toplevel(self)
                popup.geometry("750x250")
                popup_label = Label(
                    popup, text="Operation done.\n Remember to mail the updated Manifest.")
                popup_label.place(relx=.5, rely=.4, anchor=CENTER)
                confirm_button = Button(
                    popup, text="Confirm", command=lambda: on_confirm_click(popup))
                confirm_button.place(relx=.5, rely=.6, anchor=CENTER)

            def on_confirm_click(top):
                top.destroy()
                top.update()
                controller.show_frame(upload_manifest_page.UploadManifestPage)

        on_view_click()
        # view_animation = Button(self, text = "View Animation", command= lambda:on_view_click())
        # view_animation.place(relx=.5, rely=.05, anchor= CENTER)
