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
  url = f"https://check-host.net/check-tcp?host={Hostname}:{Port}&node=ir5.node.check-host.net
  &node=ir6.node.check-host.net&node=ir3.node.check-host.net&node=ir1.node.check-host.net"
  payload = {}
  headers = {'Accept': 'application/json'}

  try:
    response = requests.get(url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    request_id=json_response["request_id"]
    return request_id

  except requests.exceptions.Timeout:
      return
  except requests.exceptions.TooManyRedirects:
      return
  except requests.exceptions.RequestException as e:
      raise SystemExit(e)


def checkResult(request_id):
  url = f"https://check-host.net/check-result/{request_id}"
  payload = {}
  headers = {
    'Accept': 'application/json'
  }

  try:
    response = requests.get(url, headers=headers, data=payload)
  except requests.exceptions.Timeout:
      return
  except requests.exceptions.TooManyRedirects:
      return
  except requests.exceptions.RequestException as e:
      raise SystemExit(e)
  
  json_response = json.loads(response.text)
  keys = ["ir1.node.check-host.net", "ir3.node.check-host.net", "ir5.node.check-host.net", "ir6.node.check-host.net",]
  for key in keys:
    try:
      res = json_response[key][0]["time"]
      send_message(f"{res}")
      
    except as e:
      print(f"failed to get response due to: {e} for {json_response[key]} key")


while True:
  checkResult(checkTcp())
  time.sleep(15*60)
