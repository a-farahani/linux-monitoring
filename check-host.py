from datetime import datetime
import requests
import json
import telegram
import time
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(filename='monitoring.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


load_dotenv()
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
Hostname = os.getenv('Hostname')
Port = os.getenv('Port')


def send_message(message):
    logger.info(f"{datetime.now()}, sending message started for: {message} message")
    bot = telegram.Bot(token=TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)


def check_tcp():
    url = f"https://check-host.net/check-tcp?host={Hostname}:{Port}&node=ir5.node.check-host.net" \
        f"&node=ir6.node.check-host.net&node=ir3.node.check-host.net&node=ir1.node.check-host.net"
    payload = {}
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    request_id = json_response["request_id"]
    return request_id


def check_result(request_id):
    logger.info(f"{datetime.now()}, request_id: {request_id}")
    url = f"https://check-host.net/check-result/{request_id}"
    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers, data=payload)
    except requests.exceptions.Timeout:
        logger.warning(f"{datetime.now()}, system exited due to timeout")
        exit()
    except requests.exceptions.TooManyRedirects:
        logger.warning(f"{datetime.now()}, system exited due to TooManyRedirects")
        exit()
    except requests.exceptions.RequestException as e:
        logger.warning(f"{datetime.now()}, system exited due to {e}")
        raise SystemExit(e)

    json_response = json.loads(response.text)
    keys = ["ir1.node.check-host.net", "ir3.node.check-host.net", "ir5.node.check-host.net", "ir6.node.check-host.net"]
    for key in keys:
        try:
            result = json_response[key][0]["time"]
            send_message(f"{result}")
            logger.info(f"{datetime.now()}, message successfully sent, {key}, response: {result} ")

        except:
            logger.warning(f"{datetime.now()}, failed to get response: {json_response[key]}")
            print(f"failed to get response: {json_response[key]}")


while True:
    try:
        tcp_result = check_tcp()
        check_result(tcp_result)
        time.sleep(15*60)
    except requests.exceptions.Timeout:
        logger.warning(f"{datetime.now()}, TCP check failed due to Timeout Exception")
        exit()
    except requests.exceptions.TooManyRedirects:
        logger.warning(f"{datetime.now()}, TCP check failed due to TooManyRedirects Exception")
        exit()
    except requests.exceptions.RequestException as e:
        logger.warning(f"{datetime.now()}, TCP check failed due to RequestException Exception")
        raise exit()

