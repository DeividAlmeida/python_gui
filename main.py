import requests
from tkinter import *
from home import set_puslisher_table

window = Tk()
window.title("Designações")
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
window["bg"] = "#AC99F2"
frame = Frame(window)
frame.pack()

def get_puslisher():
  url = "http://18.117.168.254/publisher"
  payload={}
  headers = {}

  return requests.request("GET", url, headers=headers, data=payload)

res = get_puslisher()
set_puslisher_table(res, frame)

window.mainloop()

#https://www.tutorialspoint.com/delete-and-edit-items-in-tkinter-treeview