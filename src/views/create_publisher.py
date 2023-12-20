import flet as ft
from src.services import *
from src.shared.utils import *

def create_publisher_view(self):
  name=ft.TextField(label="Nome", width=500)
  type=ft.Dropdown(
    label="Nível",
    options=[
      ft.dropdown.Option(1, "Iniciante"),
      ft.dropdown.Option(2, "Intermediário"),
      ft.dropdown.Option(3, "Experiente"),
    ],
    width=500
  )
  gender=ft.Dropdown(
    label="Gênero",
    options=[
      ft.dropdown.Option("male", "Masculino"),
      ft.dropdown.Option("female", "Feminino"),
    ],
    width=500
  )
  active=ft.Switch(label="Status")
  self.page.views.append(
    ft.View(
      "/publisher",
      [
        ft.AppBar(title=ft.Text("Adicionar publicador"), bgcolor=ft.colors.SURFACE_VARIANT),
        ft.ElevatedButton("Início", on_click=lambda _: self.page.go("/")),
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
              ft.ElevatedButton("Salvar", on_click=lambda _: save(
                self,
                {
                  "name": name.value,
                  "type": int(type.value),
                  "gender": gender.value,
                  "active": bool(active.value)
                }
              )),
              ft.ElevatedButton("Cancelar", on_click=lambda _: self.page.go("/")),
            ]),
          ]),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        ),
      ],
    )
  )

def save(self, data):
  res=post_puslisher({
    "name": data["name"],
    "type": int(data["type"]),
    "gender": data["gender"],
    "active": bool(data["active"])
    })

  if res.json() == 1:
    success_bar(self)
  else:
    error_bar(self)