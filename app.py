import requests
import flet as ft
import json
publisher_id = None
rows = []

def get_puslisher():
  url = "http://18.117.168.254/publisher"
  payload = {}
  headers = {}
  return requests.request("GET", url, headers=headers, data=payload)

def patch_puslisher(data):
  url = "http://18.117.168.254/publisher/{}".format(publisher_id)
  payload = json.dumps(data)

  headers = {
    'Content-Type': 'application/json'
  }
  return requests.request("PATCH", url, headers=headers, data=payload)

def main(page: ft.Page):
  table = ft.DataTable(
    columns=[
      ft.DataColumn(ft.Text("Id")),
      ft.DataColumn(ft.Text("Nome")),
      ft.DataColumn(ft.Text("Tipo")),
      ft.DataColumn(ft.Text("Gênero")),
      ft.DataColumn(ft.Text("Qtd")),
      ft.DataColumn(ft.Text("Ativo")),
    ],
    rows=rows,
  )
  name = ft.TextField(label="Nome")
  type = ft.Dropdown(
    label="Tipo",
    options=[
        ft.dropdown.Option(1, "Novato"),
        ft.dropdown.Option(2, "Intermediário"),
        ft.dropdown.Option(3, "Experiente"),
    ],
  )

  gender = ft.Dropdown(
    label="Gênero",
    options=[
      ft.dropdown.Option("male", "Masculino"),
      ft.dropdown.Option("female", "Feminino"),
    ],
  )

  active = ft.Switch(label="Status", value=False)
  saved_alert = ft.AlertDialog(title=ft.Text("Alterações salvas!"))

  def set_table():
    global rows
    rows = []
    data = get_puslisher()
    for element  in data.json():
      rows.append(ft.DataRow(
        cells=[
          ft.DataCell(ft.Text(element['id'])),
          ft.DataCell(ft.Text(element['name'])),
          ft.DataCell(ft.Text(element['type'])),
          ft.DataCell(ft.Text(element['gender'])),
          ft.DataCell(ft.Text(element['amount'])),
          ft.DataCell(ft.Checkbox(label="",value=element['active'], disabled=True)),
        ],
        selected=True,
        data=element,
        on_select_changed=lambda e: set_values(e.control.data),
      ))
    table.rows = rows
    page.update()

  
  def init():
    set_table()
    page.add(
      ft.Row([
        ft.Container(
          table,
        ),
        ft.Column([
          ft.Container(
            name,
          ),
          ft.Container(
            type,
          ),
          ft.Container(
            gender,
          ),
          ft.Container(
            active,
          ),
          ft.Container(
            ft.ElevatedButton("Salvar", on_click=lambda e: save()),
          ),
        ]),
      ]),
      saved_alert,
    )

  def set_values(e):
    global publisher_id
    name.value = e['name']
    type.value = e['type']
    gender.value = e['gender']
    active.value = e['active']
    publisher_id = e['id']
    page.update()
  
  def save():
    res = patch_puslisher({
      "name": name.value,
      "type": int(type.value),
      "gender": gender.value,
      "active": bool(active.value)
    })

    if res.json() == 1:
      open_dlg()
    
    set_table()
    page.update()

  def open_dlg():
    page.dialog = saved_alert
    saved_alert.open = True
    page.update()

  init()

ft.app(target = main)
