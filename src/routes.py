
from src.views.create_publisher import create_publisher_view
from src.views.update_publisher import update_publisher_view
from src.views.home import home_view

def routes(self, troute):
  if troute.match("/publisher"):
    create_publisher_view(self)
  elif troute.match("/publisher/:id"):
    update_publisher_view(self, troute)
  else :
    home_view(self)