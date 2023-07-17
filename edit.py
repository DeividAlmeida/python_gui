from tkinter import ttk

def build_form(widget, publisher):
  ttk.Label(widget, text="Nome:", width=10).grid(row=0, column=0, pady=10)
  ttk.Label(widget, text="Tipo:", width=10).grid(row=1, column=0, pady=10)
  ttk.Label(widget, text="Genero:", width=10).grid(row=2, column=0, pady=10)

  name_entry = ttk.Entry(widget)
  name_entry.grid(row=0, column=1, pady=10)

  type_entry = ttk.Entry(widget)
  type_entry.grid(row=1, column=1, pady=10)

  gender_entry = ttk.Entry(widget)
  gender_entry.grid(row=2, column=1, pady=10)

  values = widget.item(publisher)["values"]
  build_default_values((name_entry, type_entry, gender_entry), values)


def build_default_values(inputs, values):
  name = values[1]
  type = values[2]
  gender = values[3]

  inputs[0].insert(0, name)
  inputs[1].insert(0, type)
  inputs[2].insert(0, gender)