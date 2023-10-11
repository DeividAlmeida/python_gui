import flet as ft
from src.services import *
from src.shared.utils import success_bar

def create_publisher_view(self):
  name = ft.TextField(label="Nome")
  type = ft.Dropdown(
    label="Nível",
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
  active = ft.Switch(label="Status")
  self.page.views.append(
    ft.View(
      "/publisher",
      [
        ft.AppBar(title=ft.Text("Adicionar publicador"), bgcolor=ft.colors.SURFACE_VARIANT),
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
              ft.ElevatedButton("Salvar", on_click=lambda e: save(
                self,
                {
                  "name": name.value,
                  "type": int(type.value),
                  "gender": gender.value,
                  "active": bool(active.value)
                }
              )),
              ft.ElevatedButton("Cancelar", on_click=lambda e: self.page.go("/")),
            ]),
          ]),
        ]),
      ],
    )
  )

def save(self, data):
  res = post_puslisher({
    "name": data["name"],
    "type": int(data["type"]),
    "gender": data["gender"],
    "active": bool(data["active"])
    })

  if res.json() == 1:
    success_bar(self)