import requests
import json
import telegram
from dotenv import load_dotenv
import os
import prettytable as pt
import time as timepack
import time
import threading

load_dotenv()
Timer = int(os.getenv('Timer'))
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
Hostname = os.getenv('Hostname')
Port = os.getenv('Port')
Nodes = json.loads(os.getenv('Nodes'))


def send_message(message):
    bot = telegram.Bot(token=TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML')


def checkTcp():
    url_node = ""
    for node in Nodes:
        url_node = url_node + f"&node={node}"
    url = f"https://check-host.net/check-tcp?host={Hostname}:{Port}{url_node}"
    payload = {}
    headers = {'Accept': 'application/json'}
    try:
        response = requests.get(url, headers=headers, data=payload)
        if response.status_code != 200:
            checkTcp()
    except:
        checkTcp()
    json_response = json.loads(response.text)
    request_id = json_response["request_id"]
    print(f"request_id: {request_id}")

    return request_id


def checkResult(request_id):
    url = f"https://check-host.net/check-result/{request_id}"
    payload = {}
    headers = {'Accept': 'application/json'}
    try:
        timepack.sleep(5)
        response = requests.get(url, headers=headers, data=payload)
        if response.status_code != 200:
            checkResult(request_id)
    except:
        checkResult(request_id)
    json_response = json.loads(response.text)
    print(f"json_response: {json_response}")

    res = f"Result: https://check-host.net/check-result/{request_id} \n\n"

    data = []
    for node in Nodes:
        if json_response[node] != "None":
            data.append((node.split(("."), 1)[
                        0], json_response[node][0]["address"], json_response[node][0]["time"]))
        else:
            data.append((node.split(("."), 1)[0], "None", "None"))

    table = pt.PrettyTable(['Node', 'Address', 'Time'])
    table.align['Node'] = 'l'
    table.align['Address'] = 'r'
    table.align['Time'] = 'r'
    for node_data, address_data, time_data in data:
        table.add_row([node_data, address_data, time_data])

    res = res + f'<pre>{table}</pre>'

    return send_message(res)


def run():
    print(time.ctime())
    request_id = checkTcp()
    checkResult(request_id)
    threading.Timer(Timer, run).start()


try:
    run()
except:
    run()
