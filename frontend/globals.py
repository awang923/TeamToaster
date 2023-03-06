from fileinput import filename
from sqlite3 import OperationalError
from wsgiref.util import shift_path_info

def init():
    global ship
    ship = {}
    global load_list
    load_list = []
    global string_filename
    string_filename = ""
    global unload_list
    unload_list = []
    global op
    op = ""
    global operations_list
    operations_list = []


#def get_filename():
    #test = lambda: string_filename
    #return test