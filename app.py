
import flet as ft
from src.services import *

class Main:
  saved_alert = ft.AlertDialog(title=ft.Text("Alterações salvas!"))
  snack_bar = ft.SnackBar(
      content="Designações geradas com sucesso!",
      action="All Done",
  )
  def __init__(self, page: ft.Page):
    self.page = page
    self.page.title = "Controle de designações"
    self.page.on_route_change = self.route_change()
    self.page.on_view_pop = self.view_pop
    self.page.go(self.page.route)

  def close_dlg(self, e):
    self.page.dialog.open = False
    self.page.update()

  def delete(self, id):
    res = delete_puslisher(id)
    if res.json() == 1:
        self.close_dlg(None)
        self.page.go("/")

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

  def route_change(self):
    troute = ft.TemplateRoute(self.page.route)
    self.page.views.clear()
    
    if troute.match("/publisher"):
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
                ft.Container(
                  ft.ElevatedButton("Salvar", on_click=lambda e: self.save(
                    {
                      "name": name.value,
                      "type": int(type.value),
                      "gender": gender.value,
                      "active": bool(active.value)
                    }
                  )),
                ),
              ]),
            ]),
          ],
        )
      )
    
    elif troute.match("/publisher/:id"):
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
                  ft.ElevatedButton("Editar", on_click=lambda e: self.edit(
                    {
                      "name": name.value,
                      "type": int(type.value),
                      "gender": gender.value,
                      "active": bool(active.value)
                    },
                    troute.id
                  )),
                  ft.ElevatedButton("Deletar", on_click=lambda e: self.open_dlg_modal(
                    troute.id
                  )),
                ]),
              ]),
            ]),
          ],
        )
      )
    else :
      self.page.views.append(
        ft.View(
          "/",
          [
            ft.AppBar(title=ft.Text("Lista de publicadores"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Row([
              ft.ElevatedButton("Adicionar Publicador", on_click=lambda _: self.page.go("/publisher")),
              ft.ElevatedButton("Gerar Designações", on_click=lambda _: self.open_designations_config()),
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
              rows=self.set_table(),
            ),
          ],
        )
      )

    self.page.update()

  def view_pop(self):
    self.page.views.pop()
    if len(self.page.views) > 0:
      top_view = self.page.views[-1]
      self.page.go(top_view.route)
  
  def edit(self, data, id):
    res = patch_puslisher(data, id)
    if res.json() == 1:
      self.open_dlg()
        
  def save(self, data):
    res = post_puslisher({
      "name": data["name"],
      "type": int(data["type"]),
      "gender": data["gender"],
      "active": bool(data["active"])
      })

    if res.json() == 1:
      self.open_dlg()
  
  def open_dlg(self):
    self.page.dialog = self.saved_alert
    self.saved_alert.open = True
    self.page.update()

  def open_dlg_modal(self, id):
    self.page.dialog = ft.AlertDialog(
    modal=True,
    title=ft.Text("Atenção!!"),
    content=ft.Text("Tem certeza que deseja excluir?"),
    actions=[
        ft.TextButton("Não", on_click=lambda e: self.close_dlg(e)),
        ft.TextButton("Sim", on_click= lambda e: self.delete(id)),
    ],
  )
    self.page.dialog.open = True
    self.page.update()

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
          ft.TextButton("Cancelar", on_click=lambda e: self.close_dlg(e)),
          ft.TextButton("Gerar", on_click=lambda e: (get_designations(gender.value, length.value), self.close_dlg(e), self.snack_bar())),
        ]),
      ],
    )
    self.page.dialog.open = True
    self.page.update()

  def snack_bar(self):
    self.page.snack_bar = ft.SnackBar(ft.Text("Designações geradas com sucesso!"))
    self.page.snack_bar.open = True
    self.page.update()


ft.app(target=Main, view=ft.AppView.FLET_APP)