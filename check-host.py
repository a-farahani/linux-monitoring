import requests
import json

Hostname = "cfvmger01.stopstops.top"
Port = 443

url = f"""https://check-host.net/check-tcp?host={Hostname}:{Port}&node=ir5.node.check-host.net&node=ir6.node.check-host.net&node=ir3.node.check-host.net&node=ir1.node.check-host.net"""

payload = {}
headers = {
  'Accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

json_response = json.loads(response.text)
# print(json_response)

permanent_link=json_response["permanent_link"]
permanent_link_id=permanent_link.rpartition('/')[-1] # check before split
# print(permanent_link_id)


url = f"https://check-host.net/check-result/{permanent_link_id}"

payload = {}
headers = {
  'Accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

# json_response = json.loads(response.text)
# print(json_response["ir1.node.check-host.net"])
# print(json_response["ir3.node.check-host.net"])
