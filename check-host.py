import requests
import json
import telegram
from dotenv import load_dotenv
import os
import prettytable as pt
import time


load_dotenv()
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
Hostname = os.getenv('Hostname')
Port = os.getenv('Port')

def send_message(message):
    bot = telegram.Bot(token=TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML')

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

  return request_id or 0

def checkResult(request_id):

  if request_id == 0:
     checkResult(checkTcp())
     return
  
  url = f"https://check-host.net/check-result/{request_id}"
  payload = {}
  headers = {
    'Accept': 'application/json'
  }

  try:
    time.sleep(10)
    response = requests.get(url, headers=headers, data=payload)
  except requests.exceptions.Timeout:
      exit
  except requests.exceptions.TooManyRedirects:
      exit
  except requests.exceptions.RequestException as e:
      raise SystemExit(e)
  
  json_response = json.loads(response.text)


  res = f"Result: https://check-host.net/check-result/{request_id} \n\n"

  table = pt.PrettyTable(['Name', 'Time'])
  table.align['Name'] = 'l'
  table.align['Time'] = 'r'
  data = [
      ('ir1', json_response["ir1.node.check-host.net"][0]["time"]),
      ('ir3', json_response["ir3.node.check-host.net"][0]["time"]),
      ('ir4', json_response["ir5.node.check-host.net"][0]["time"]),
      ('ir6', json_response["ir6.node.check-host.net"][0]["time"]),
  ]
  for name, time1 in data:
      table.add_row([name, time1])

  res = res + f'<pre>{table}</pre>'
  send_message(res)

while True:
  checkResult(checkTcp())
  time.sleep(15*60)
