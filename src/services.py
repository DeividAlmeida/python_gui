import requests
import json
import pandas as pd
import datetime
from openpyxl.workbook import Workbook
server = "http://18.117.168.254"

def get_puslishers():
  url = "{}/publisher".format(server)
  payload = {}
  headers = {}
  return requests.request("GET", url, headers=headers, data=payload)

def get_puslisher(publisher_id):
  url = "{}/publisher/{}".format(server, publisher_id)
  payload = {}
  headers = {}
  return requests.request("GET", url, headers=headers, data=payload)

def patch_puslisher(data, publisher_id):
  url = "{}/publisher/{}".format(server, publisher_id)
  payload = json.dumps(data)
  headers = {
    "Content-Type": "application/json"
  }
  return requests.request("PATCH", url, headers=headers, data=payload)

def post_puslisher(data):
  url = "{}/publisher".format(server)
  payload = json.dumps(data)
  headers = {
    "Content-Type": "application/json"
  }
  return requests.request("POST", url, headers=headers, data=payload)

def delete_puslisher(publisher_id):
  url = "{}/publisher/{}".format(server, publisher_id)
  payload = {}
  headers = {}
  return requests.request("DELETE", url, headers=headers, data=payload)

def get_designations(gender, length):
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
    generate_designations(res.json())
    
  except:
    length = 1

def generate_designations(data):
  mains = []
  helpers = []
  for element in data:
    mains.append(element[0]["name"])
    helpers.append(element[1]["name"])
  
  pd.DataFrame({"Principal": mains,"Ajudante": helpers}).to_excel("designations/{}.xlsx".format(datetime.datetime.now()), index=False)
