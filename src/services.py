import requests
import json
import pandas as pd
import datetime
from openpyxl.workbook import Workbook
from src.shared.utils import success_bar, error_bar

server = "http://18.117.168.254"

def get_puslishers():
  try:
    url = "{}/publisher".format(server)
    payload = {}
    headers = {}
    return requests.request("GET", url, headers=headers, data=payload)
  except:
    return []

def get_puslisher(publisher_id):
  try:
    url = "{}/publisher/{}".format(server, publisher_id)
    payload = {}
    headers = {}
    return requests.request("GET", url, headers=headers, data=payload)
  except:
    return []

def patch_puslisher(data, publisher_id):
  try:
    url = "{}/publisher/{}".format(server, publisher_id)
    payload = json.dumps(data)
    headers = {
      "Content-Type": "application/json"
    }
    return requests.request("PATCH", url, headers=headers, data=payload)
  except:
    return []

def post_puslisher(data):
  try:
    url = "{}/publisher".format(server)
    payload = json.dumps(data)
    headers = {
      "Content-Type": "application/json"
    }
    return requests.request("POST", url, headers=headers, data=payload)
  except:
    return 0

def delete_puslisher(publisher_id):
  try:
    url = "{}/publisher/{}".format(server, publisher_id)
    payload = {}
    headers = {}
    return requests.request("DELETE", url, headers=headers, data=payload)
  except:
    return 0

def get_designations(self, gender, length):
  try:
    length = int(length)
    url = "{}/presentations".format(server)
    payload = json.dumps({
      "length": length,
      "gender": gender
    })
    headers = {
      "Content-Type": "application/json"
    }
    res = requests.request("POST", url, headers=headers, data=payload)
    generate_designations(self, res.json())
  except:
    error_bar(self)

def generate_designations(self, data):
  try:
    mains = []
    helpers = []
    for element in data:
      mains.append(element[0]["name"])
      helpers.append(element[1]["name"])
    pd.DataFrame({"Principal": mains,"Ajudante": helpers}).to_excel("designations/{}.xlsx".format(datetime.datetime.now()), index=False)
    success_bar(self)
  except:
    error_bar(self)
