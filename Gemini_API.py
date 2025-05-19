'''

save secrets.py first:
'''

import network, socket
import urequests as requests
import ujson
from time import sleep
from secrets import *

url = query_url  # from secrets

# Chat history (resets on restart)
chat_history = []

def connect_to_wifi():
    ssid = wifi_ssid
    password = wifi_password
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        print('connecting to network...')
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            print('.', end='')
            sleep(0.25)
    try:
        host = sta_if.config('hostname')
    except ValueError:
        host = sta_if.config('dhcp_hostname')
    print('Wifi connected as {}/{}, net={}, gw={}, dns={}'.format(host, *sta_if.ifconfig()))

def query(query, ask_user=False):
    global chat_history

    if ask_user:
        question = input("Type: ")
    else:
        question = query

    # Add user message to history
    chat_history.append({
        "role": "user",
        "parts": [{"text": str(question)}]
    })

    payload = ujson.dumps({
        "contents": chat_history
    })

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response_data = response.json()
        message = response_data["candidates"][0]["content"]["parts"][0]["text"]

        chat_history.append({
            "role": "model",
            "parts": [{"text": message}]
        })

    except Exception as e:
        message = f"[Error: {e}\n reply: {response_data}]"
    finally:
        response.close()
    return message

