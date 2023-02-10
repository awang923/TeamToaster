import tkinter as tk
from tkinter import *
from tkinter import filedialog
from select_op_page import SelectOperationPage

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