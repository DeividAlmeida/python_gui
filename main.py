import requests
from tkinter import *
from  tkinter import ttk

def get_puslisher():
  url = "http://18.117.168.254/publisher"
  payload={}
  headers = {}

  return requests.request("GET", url, headers=headers, data=payload)

def set_puslisher_table(response):
  frame = Frame(window)
  frame.pack()
  table = ttk.Treeview(frame)
  table["columns"] = ("id", "name", "type", "gender", "amount")

  table.column("#0", width=0,  stretch=NO)
  table.column("id",anchor=CENTER, width=80)
  table.column("name",anchor=CENTER,width=160)
  table.column("type",anchor=CENTER,width=80)
  table.column("gender",anchor=CENTER,width=80)
  table.column("amount",anchor=CENTER,width=80)

  table.heading("#0",text="",anchor=CENTER)
  table.heading("id",text="Id",anchor=CENTER)
  table.heading("name",text="Nome",anchor=CENTER)
  table.heading("type",text="Tipo",anchor=CENTER)
  table.heading("gender",text="Gênero",anchor=CENTER)
  table.heading("amount",text="Qtd",anchor=CENTER)

  i=0
  for element  in response.json():
    table.insert(parent="",index="end",iid=i,text="",
    values=(element["id"], element["name"],element["type"],element["gender"], element["amount"]))
    i+=1

  table.pack()


window = Tk()
window.title("Designações")
window.geometry("500x500")
window["bg"] = "#AC99F2"

res = get_puslisher()
set_puslisher_table(res)

window.mainloop()