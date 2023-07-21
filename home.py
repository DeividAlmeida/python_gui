from tkinter import *
from tkinter import ttk
from edit import build_form

def edit(event, table):
  widget = event.widget
  publisher = widget.identify("item", event.x, event.y)
  build_form(widget, publisher)

def set_puslisher_table(response, frame):
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
    values=(element["id"], element["name"],element["type"],element["gender"], element["amount"], "kj"))
    table.bind("<ButtonRelease-1>", lambda event, col=1: edit(event, table))
    i+=1
  table.pack()
  ttk.Label(frame, text="Nome:", width=10).pack()
  ttk.Entry(frame).pack()
  ttk.Label(frame, text="Tipo:", width=10).pack()
  ttk.Entry(frame).pack()
  ttk.Label(frame, text="Genero:", width=10).pack()
  ttk.Entry(frame).pack()

  ttk.Button(frame, text="Editar").pack(side=LEFT)
  ttk.Button(frame, text="Deletar").pack()
  ttk.Button(frame, text="Gerar Relório").pack(side=RIGHT)
