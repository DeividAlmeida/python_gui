import requests
import flet as ft
import json

def get_puslishers():
  url = "http://18.117.168.254/publisher"
  payload = {}
  headers = {}
  return requests.request("GET", url, headers=headers, data=payload)

def get_puslisher(publisher_id):
  url = "http://18.117.168.254/publisher/{}".format(publisher_id)
  payload = {}
  headers = {}
  return requests.request("GET", url, headers=headers, data=payload)

def patch_puslisher(data, publisher_id):
  url = "http://18.117.168.254/publisher/{}".format(publisher_id)
  payload = json.dumps(data)

  headers = {
    'Content-Type': 'application/json'
  }
  return requests.request("PATCH", url, headers=headers, data=payload)

def post_puslisher(data):
  url = "http://18.117.168.254/publisher"
  payload = json.dumps(data)

  headers = {
    'Content-Type': 'application/json'
  }
  return requests.request("POST", url, headers=headers, data=payload)

def delete_puslisher(publisher_id):
  url = "http://18.117.168.254/publisher/{}".format(publisher_id)
  payload = {}
  headers = {}

  return requests.request("DELETE", url, headers=headers, data=payload)

def main(page: ft.Page):

  def close_dlg(e):
    page.dialog.open = False
    page.update()

  def delete(id):
    res = delete_puslisher(id)
    if res.json() == 1:
      close_dlg(None)
      page.go("/")

  page.title = "Routes Example"
  saved_alert = ft.AlertDialog(title=ft.Text("Alterações salvas!"))

  def set_table():
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
            on_select_changed=lambda e: page.go("/publisher/{}".format(e.control.data["id"])),
          )
        )
      return rows

  def route_change(route):
      troute = ft.TemplateRoute(page.route)
      page.views.clear()
      page.views.append(
        ft.View(
          "/",
          [
            ft.AppBar(title=ft.Text("Lista de publicadores"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.ElevatedButton("Adicionar Publicador", on_click=lambda _: page.go("/publisher")),
            ft.DataTable(
              columns=[
                ft.DataColumn(ft.Text("Id")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Gênero")),
                ft.DataColumn(ft.Text("Qtd")),
                ft.DataColumn(ft.Text("Ativo")),
              ],
              rows=set_table(),
            ),
          ],
        )
      )
      
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
        page.views.append(
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
                    ft.ElevatedButton("Salvar", on_click=lambda e: save(
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
      
      if troute.match("/publisher/:id"):
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
        page.views.append(
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
                      {
                        "name": name.value,
                        "type": int(type.value),
                        "gender": gender.value,
                        "active": bool(active.value)
                      },
                      troute.id
                    )),
                    ft.ElevatedButton("Deletar", on_click=lambda e: open_dlg_modal(
                      troute.id
                    )),
                  ]),
                ]),
              ]),
            ],
          )
        )
      
      page.update()

  def view_pop(view):
    page.views.pop()
    if len(page.views) > 0:
      top_view = page.views[-1]
      page.go(top_view.route)
  
  def edit(data, id):
    res = patch_puslisher(data, id)
    if res.json() == 1:
      open_dlg()
        
  def save(data):
    res = post_puslisher({
      "name": data["name"],
      "type": int(data["type"]),
      "gender": data["gender"],
      "active": bool(data["active"])
      })

    if res.json() == 1:
      open_dlg()
  
  def open_dlg():
    page.dialog = saved_alert
    saved_alert.open = True
    page.update()

  def open_dlg_modal(id):
    page.dialog = ft.AlertDialog(
    modal=True,
    title=ft.Text("Atenção!!"),
    content=ft.Text("Tem certeza que deseja excluir?"),
    actions=[
        ft.TextButton("Não", on_click=lambda e: close_dlg(e)),
        ft.TextButton("Sim", on_click= lambda e: delete(id)),
    ],
    on_dismiss=lambda e: print("Modal dialog dismissed!"),
  )
    page.dialog.open = True
    page.update()


  page.on_route_change = route_change
  page.on_view_pop = view_pop
  page.go(page.route)


ft.app(target=main, view=ft.AppView.FLET_APP)