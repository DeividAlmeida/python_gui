import flet as ft
from src.services import *
from src.routes import routes

class Main:
  def __init__(self, page: ft.Page):
    self.page=page
    self.page.title="Controle de designações"
    self.page.on_route_change=self.route_change
    self.page.on_view_pop=self.view_pop
    self.page.scroll=True

    self.page.go(self.page.route)

  def route_change(self, route):
    troute=ft.TemplateRoute(self.page.route)
    self.page.views.clear()
    routes(self, troute)
    self.page.update()

  def view_pop(self):
    self.page.views.pop()
    if len(self.page.views) > 0:
      top_view=self.page.views[-1]
      self.page.go(top_view.route)
  
ft.app(target=Main, view=ft.AppView.FLET_APP)