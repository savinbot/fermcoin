import requests
import json


track_url = 'https://api.botan.io/track'


def make_json(message):
    data = {}
    data['message_id'] = message.message_id
    data['from'] = {}
    data['from']['id'] = message.from_user.id
    if message.from_user.username is not None:
        data['from']['username'] = message.from_user.username
    data['chat'] = {}
    data['chat']['id'] = message.chat.id
    return data


def track(token, uid, message, name='Message'):
    try:
        r = requests.post(
            track_url,
            params={"token": token, "uid": uid, "name": name},
            data=make_json(message),
            headers={'Content-type': 'application/json'},
        )
        return r.json()
    except:
        return False
