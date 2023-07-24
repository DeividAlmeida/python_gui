from tkinter import *
from tkinter import ttk
from  window import frame
selected = None

ttk.Label(frame, text="Nome:", width=10).grid(row=0, column=0, pady=10)
name = ttk.Entry(frame)
name.grid(row=0, column=1, pady=10)

ttk.Label(frame, text="Tipo:", width=10).grid(row=1, column=0, pady=10)
type = ttk.Entry(frame)
type.grid(row=1, column=1, pady=10)

ttk.Label(frame, text="Genero:", width=10).grid(row=2, column=0, pady=10)
gender = ttk.Entry(frame)
gender.grid(row=2, column=1, pady=10)


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
table.grid(row=4, column=0, columnspan=3, pady=10)


def edit():
  row_selected = table.selection()[selected]
  id = table.item(row_selected)["values"][selected]
  name_value = name.get()
  type_value = type.get()
  gender_value = gender.get()
  table.item(row_selected, text="blub", values=(id, name_value, type_value, gender_value))

ttk.Button(frame, text="Editar", command=edit).grid(row=3, column=0, pady=10)
ttk.Button(frame, text="Deletar").grid(row=3, column=1, pady=10)
ttk.Button(frame, text="Gerar Relório").grid(row=3, column=2, pady=10)


def select(event):
  widget = event.widget
  global selected
  selected = int(widget.identify("item", event.x, event.y))

  name.delete(0, END)
  name.insert(0, widget.item(selected)["values"][1])

  type.delete(0, END)
  type.insert(0, widget.item(selected)["values"][2])

  gender.delete(0, END)
  gender.insert(0, widget.item(selected)["values"][3])


def set_puslisher_table(response):
  i=0
  for element  in response.json():

    table.insert(parent="",index="end",iid=i,text="",
    values=(element["id"], element["name"],element["type"],element["gender"], element["amount"]))
    table.bind("<ButtonRelease-1>", lambda event, col=1: select(event))
    i+=1
