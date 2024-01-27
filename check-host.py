import requests
import json
import telegram
import time
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
Hostname = os.getenv('Hostname')
Port = os.getenv('Port')

def send_message(message):
    bot = telegram.Bot(token=TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

def checkTcp():
  url = f"""https://check-host.net/check-tcp?host={Hostname}:{Port}&node=ir5.node.check-host.net&node=ir6.node.check-host.net&node=ir3.node.check-host.net&node=ir1.node.check-host.net"""
  payload = {}
  headers = {
    'Accept': 'application/json'
  }

  try:
    response = requests.get(url, headers=headers, data=payload)
  except requests.exceptions.Timeout:
      exit
  except requests.exceptions.TooManyRedirects:
      exit
  except requests.exceptions.RequestException as e:
      raise SystemExit(e)
  json_response = json.loads(response.text)
  request_id=json_response["request_id"]

  return request_id

def checkResult(request_id):
  url = f"https://check-host.net/check-result/{request_id}"
  payload = {}
  headers = {
    'Accept': 'application/json'
  }

  try:
    response = requests.get(url, headers=headers, data=payload)
  except requests.exceptions.Timeout:
      exit
  except requests.exceptions.TooManyRedirects:
      exit
  except requests.exceptions.RequestException as e:
      raise SystemExit(e)
  
  json_response = json.loads(response.text)
  try:
    res1 = json_response["ir1.node.check-host.net"][0]["time"]
    send_message(f"ir1 {res1}")
  except:
      print(json_response["ir1.node.check-host.net"])
  try:
    res3 = json_response["ir3.node.check-host.net"][0]["time"]
    send_message(f"ir3 {res3}")
  except:
      print(json_response["ir3.node.check-host.net"])
  try:
    res5 = json_response["ir5.node.check-host.net"][0]["time"]
    send_message(f"ir5 {res5}")
  except:
      print(json_response["ir5.node.check-host.net"])
  try:
    res6 = json_response["ir6.node.check-host.net"][0]["time"]
    send_message(f"ir6 {res6}")
  except:
      print(json_response["ir6.node.check-host.net"])

while True:
  checkResult(checkTcp())
  time.sleep(15*60)
