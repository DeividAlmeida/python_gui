import requests
from view import set_puslisher_table
from  window import *

def get_puslisher():
  url = "http://18.117.168.254/publisher"
  payload = {}
  headers = {}

  return requests.request("GET", url, headers=headers, data=payload)

res = get_puslisher()
set_puslisher_table(res)

window.mainloop()

#https://www.tutorialspoint.com/delete-and-edit-items-in-tkinter-treeview