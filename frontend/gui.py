import tkinter as tk
from tkinter import *
from login_page import LoginPage
from select_op_page import SelectOperationPage
from upload_manifest_page import UploadManifestPage
from load_page import InputLoadPage
from unload_page import InputUnloadPage
from computing_page import ComputingPage
from operation import Operation
import globals

globals.init()

class Application(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, minsize=800)
		container.grid_columnconfigure(0, minsize=1000)

		self.frames = {}
		for F in (LoginPage, UploadManifestPage, SelectOperationPage, InputLoadPage, InputUnloadPage, ComputingPage, Operation):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row = 0, column = 0, sticky ="nsew")
		self.show_frame(LoginPage)
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

app = Application()
app.mainloop()
# root.mainloop()