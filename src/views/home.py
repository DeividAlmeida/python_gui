import flet as ft
from src.services import *
from src.shared.utils import *
from src.shared.paginated_dt import PaginatedDataTable

def home_view(self):
  self.page.views.append(
    ft.View(
      "/",
      [
        ft.AppBar(title=ft.Text("Lista de publicadores"), bgcolor = ft.colors.SURFACE_VARIANT),
        ft.Row([
          ft.ElevatedButton("Adicionar Publicador", on_click = lambda _: self.page.go("/publisher")),
          ft.ElevatedButton("Gerar Designações", on_click = lambda _: open_designations_config(self)),
        ]),
        PaginatedDataTable(
          ft.DataTable(
            width = 1700,
            columns = [
              ft.DataColumn(ft.Text("Id")),
              ft.DataColumn(ft.Text("Nome")),
              ft.DataColumn(ft.Text("Tipo")),
              ft.DataColumn(ft.Text("Gênero")),
              ft.DataColumn(ft.Text("Qtd")),
              ft.DataColumn(ft.Text("Ativo")),
            ],
            divider_thickness=3,
            rows=set_table(self),
          ),
          rows_per_page = 10,
          width = 1700,
        ),
      ],
    )
  )

def set_table(self):
  global translates
  rows = []
  data = get_puslishers()
  for element  in data.json():
    rows.append(
      ft.DataRow(
        cells = [
          ft.DataCell(ft.Text(element["id"])),
          ft.DataCell(ft.Text(element["name"])),
          ft.DataCell(ft.Text(translates["TYPE"][element["type"]])),
          ft.DataCell(ft.Text(translates["GENDER"][element["gender"]])),
          ft.DataCell(ft.Text(element["amount"])),
          ft.DataCell(ft.Checkbox(label = "",value = element["active"], disabled = True)),
        ],
        selected = True,
        data = element,
        on_select_changed = lambda e: self.page.go("/publisher/{}".format(e.control.data["id"])),
      )
    )
  return rows

def open_designations_config(self):
  gender = ft.Dropdown(
    label = "Gênero",
    value = "female",
    options = [
      ft.dropdown.Option("male", "Masculino"),
      ft.dropdown.Option("female", "Feminino"),
    ],
  )
  length = ft.TextField(label="Quantidade", hint_text="Quantidade máxima 255")
  self.page.dialog = ft.AlertDialog(
    modal = True,
    title = ft.Text("Coloque a quantidade de designações e o género dos designados"),
    actions = [
      ft.Container(
        gender,
        margin = ft.Margin(10, 10, 10, 10),
      ),
      ft.Container(
        length,
        margin = ft.Margin(10, 10, 10, 10),
      ),
      ft.Row([
        ft.TextButton("Cancelar", on_click = lambda _: close_dlg(self)),
        ft.TextButton("Gerar", on_click = lambda _: (close_dlg(self), get_designations(self, gender.value, length.value))),
      ]),
    ],
  )
  self.page.dialog.open = True
  self.page.update()