import flet as ft
from src.services import *
from src.shared.utils import *

def update_publisher_view(self, troute):
  puslisher = get_puslisher(troute.id).json()
  name = ft.TextField(label="Nome", value=puslisher["name"], width = 500)
  type = ft.Dropdown(
    label = "Nível",
    value = puslisher["type"],
    options = [
      ft.dropdown.Option(1, "Iniciante"),
      ft.dropdown.Option(2, "Intermediário"),
      ft.dropdown.Option(3, "Experiente"),
    ],
    width = 500
  )
  gender = ft.Dropdown(
    label = "Gênero",
    value = puslisher["gender"],
    options = [
      ft.dropdown.Option("male", "Masculino"),
      ft.dropdown.Option("female", "Feminino"),
    ],
    width = 500
  )
  active = ft.Switch(label = "Status", value = puslisher["active"])
  self.page.views.append(
    ft.View(
      "/publisher/:id",
      [
        ft.AppBar(title = ft.Text("Editar {}".format(puslisher["name"])), bgcolor = ft.colors.SURFACE_VARIANT),
        ft.ElevatedButton("Início", on_click = lambda _: self.page.go("/")),
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
              ft.ElevatedButton("Editar", on_click = lambda _: edit(
                self,
                {
                  "name": name.value,
                  "type": int(type.value),
                  "gender": gender.value,
                  "active": bool(active.value)
                },
                troute.id
              )),
              ft.ElevatedButton("Deletar", on_click = lambda _: open_dlg_modal(
                self,
                troute.id
              )),
              ft.ElevatedButton("Cancelar", on_click = lambda _: self.page.go("/")),
            ]),
          ]),
        ],
        alignment = ft.MainAxisAlignment.CENTER,
        ),
      ],
    )
  )

def open_dlg_modal(self, id):
  self.page.dialog = ft.AlertDialog(
    modal=True,
    title=ft.Text("Atenção!!"),
    content=ft.Text("Tem certeza que deseja excluir?"),
    actions=[
      ft.TextButton("Não", on_click = lambda _: close_dlg(self)),
      ft.TextButton("Sim", on_click = lambda _: delete(self, id)),
    ],
  )
  self.page.dialog.open = True
  self.page.update()

def edit(self, data, id):
  res = patch_puslisher(data, id)
  if res.json() == 1:
    self.page.go("/")
    success_bar(self)
  else:
    error_bar(self)
      
def delete(self, id):
  res = delete_puslisher(id)
  close_dlg(self)
  if res.json() == 1:
    self.page.go("/")
    success_bar(self)
  else:
    error_bar(self)