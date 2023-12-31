import flet as ft

def success_bar(self):
  self.page.snack_bar=ft.SnackBar(
    ft.Text("Deu tudo certo!"),
    bgcolor=ft.colors.GREEN_300,
  )
  self.page.snack_bar.open=True
  self.page.update()

def error_bar(self):
  self.page.snack_bar=ft.SnackBar(
    ft.Text("Algo deu errado!"),
    bgcolor=ft.colors.RED_300,
  )
  self.page.snack_bar.open=True
  self.page.update()

def close_dlg(self):
  self.page.dialog.open=False
  self.page.update()

translates={
  "TYPE" : ["", "Iniciante", "Intermediário", "Experiente"],
  "GENDER" : {
    "male" : "Masculino",
    "female" : "Feminino",
  }
}