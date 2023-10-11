import flet as ft
from src.services import *
from src.shared.utils import *

def home_view(self):
  self.page.views.append(
    ft.View(
      "/",
      [
        ft.AppBar(title=ft.Text("Lista de publicadores"), bgcolor=ft.colors.SURFACE_VARIANT),
        ft.Row([
          ft.ElevatedButton("Adicionar Publicador", on_click=lambda _: self.page.go("/publisher")),
          ft.ElevatedButton("Gerar Designações", on_click=lambda _: open_designations_config(self)),
        ]),
        ft.DataTable(
          columns=[
            ft.DataColumn(ft.Text("Id")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Gênero")),
            ft.DataColumn(ft.Text("Qtd")),
            ft.DataColumn(ft.Text("Ativo")),
          ],
          rows=set_table(self),
        ),
      ],
    )
  )

def set_table(self):
  rows = []
  data = get_puslishers()
  for element  in data.json():
    rows.append(
      ft.DataRow(
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
        on_select_changed=lambda e: self.page.go("/publisher/{}".format(e.control.data["id"])),
      )
    )
  return rows

def open_designations_config(self):
  gender = ft.Dropdown(
    label="Gênero",
    value="female",
    options=[
      ft.dropdown.Option("male", "Masculino"),
      ft.dropdown.Option("female", "Feminino"),
    ],
  )
  length = ft.TextField(label="Quantidade")
  self.page.dialog = ft.AlertDialog(
    modal=True,
    title=ft.Text("Configurações de designações"),
    content=ft.Text("Coloque a quantidade de designações e o genero dos designados"),
    actions=[
      ft.Container(
        gender,
        margin=ft.Margin(10, 10, 10, 10),
      ),
      ft.Container(
        length,
        margin=ft.Margin(10, 10, 10, 10),
      ),
      ft.Row([
        ft.TextButton("Cancelar", on_click=lambda e: close_dlg(self)),
        ft.TextButton("Gerar", on_click=lambda e: (get_designations(gender.value, length.value), close_dlg(self), success_bar())),
      ]),
    ],
  )
  self.page.dialog.open = True
  self.page.update()