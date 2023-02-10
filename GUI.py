import tkinter as tk
from tkinter import *
from tkinter import filedialog
# root = tk.Tk()
# root.geometry("400x500")

class Application(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, minsize=400)
		container.grid_columnconfigure(0, minsize=500)

		self.frames = {}
		for F in (LoginPage, UploadManifestPage, SelectOperationPage, InputLoadPage, InputUnloadPage):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row = 0, column = 0, sticky ="nsew")
		self.show_frame(LoginPage)
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

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
        username_input.place(relx=.5, rely=.2, anchor= CENTER)
        
        # def show_signin_button():
        sign_in_button = Button(self, text="Sign In", command=lambda: controller.show_frame(UploadManifestPage) if username_input.get() !='' else open_error_popup(), width=20)
        sign_in_button.place(relx=.5, rely=.4, anchor= CENTER)

        
        # def onclick_sign_in():
        #     sign_in_msg = Label(root, text="Hello " + username_input.get(), fg='black')
        #     sign_in_msg.pack()
        def open_error_popup():
            error_msg = Label(self, text="Enter your first name and last name")
            error_msg.place(relx=.5, rely=.3, anchor= CENTER)

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

       

class UploadManifestPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        upload_prompt = Label(self, text = "Please upload the manifest")
        upload_prompt.place(relx=.5, rely=.1, anchor= CENTER)

        def open_file():
        # global file
            self.filename = filedialog.askopenfilename(title = "Select File", filetypes=(("txt file", "*.txt"),))
            filename_label = Label(self, text = self.filename)
            filename_label.place(relx=.5, rely=.3, anchor= CENTER)

        upload_button = Button(self, text="Select File", command=open_file)
        upload_button.place(relx=.5, rely=.2, anchor= CENTER)

        done_button = Button(self, text="DONE", command=lambda: controller.show_frame(SelectOperationPage))
        done_button.place(rely=.9, relx=.9, anchor=SE)

    
class SelectOperationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        selection_prompt = Label(self, text = "Please select an operation")
        selection_prompt.place(relx=.5, rely=.1, anchor= CENTER)

        load_button = Button(self, text="Load/Unload", command=lambda: controller.show_frame(InputLoadPage), width=20)
        load_button.place(relx=.25, rely=.2, anchor= CENTER)        
        balance_button = Button(self, text="Balance", command=lambda: controller.show_frame(ComputingPage), width=20)
        balance_button.place(relx=.75, rely=.2, anchor= CENTER)        

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
            self.y += 0.1
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


class InputUnloadPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        unload_prompt = Label(self, text = "Please input all containers to be unloaded")
        unload_prompt.place(relx=.5, rely=.1, anchor= CENTER)

class ComputingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        load_prompt = Label(self, text = "Please input all containers to be loaded")
        load_prompt.place(relx=.5, rely=.1, anchor= CENTER)



app = Application()
app.mainloop()
# root.mainloop()