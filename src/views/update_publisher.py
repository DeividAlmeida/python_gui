import flet as ft
from src.services import *
from src.shared.utils import *

def update_publisher_view(self, troute):
  puslisher = get_puslisher(troute.id).json()
  name = ft.TextField(label="Nome", value=puslisher["name"])
  type = ft.Dropdown(
    label="Nível",
    value=puslisher["type"],
    options=[
      ft.dropdown.Option(1, "Novato"),
      ft.dropdown.Option(2, "Intermediário"),
      ft.dropdown.Option(3, "Experiente"),
    ],
  )
  gender = ft.Dropdown(
    label="Gênero",
    value=puslisher["gender"],
    options=[
      ft.dropdown.Option("male", "Masculino"),
      ft.dropdown.Option("female", "Feminino"),
    ],
  )
  active = ft.Switch(label="Status", value=puslisher["active"])
  self.page.views.append(
    ft.View(
      "/publisher/:id",
      [
        ft.AppBar(title=ft.Text(troute.id), bgcolor=ft.colors.SURFACE_VARIANT),
        ft.Row([
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
            ft.Row([
              ft.ElevatedButton("Editar", on_click=lambda e: edit(
                self,
                {
                  "name": name.value,
                  "type": int(type.value),
                  "gender": gender.value,
                  "active": bool(active.value)
                },
                troute.id
              )),
              ft.ElevatedButton("Deletar", on_click=lambda e: open_dlg_modal(
                self,
                troute.id
              )),
              ft.ElevatedButton("Cancelar", on_click=lambda e: self.page.go("/")),
            ]),
          ]),
        ]),
      ],
    )
  )

def open_dlg_modal(self, id):
  self.page.dialog = ft.AlertDialog(
    modal=True,
    title=ft.Text("Atenção!!"),
    content=ft.Text("Tem certeza que deseja excluir?"),
    actions=[
      ft.TextButton("Não", on_click=lambda e: close_dlg(self)),
      ft.TextButton("Sim", on_click= lambda e: delete(id)),
    ],
  )
  self.page.dialog.open = True
  self.page.update()

def edit(self, data, id):
  res = patch_puslisher(data, id)
  if res.json() == 1:
    success_bar(self)
      
def delete(self, id):
  res = delete_puslisher(id)
  if res.json() == 1:
    close_dlg(self)
    self.page.go("/")