import time
import json
import requests
import urllib.parse


# Super secret - Shhhh
UAID = "ua_01B5C47165D547DDB157CD5E3E6DA200"
SECRET_KEY = ""  # REDACTED
API_BASE_URL = "https://api.yosmart.com"  # open/yolink/v2/api
API_TOKEN_URL = f"{API_BASE_URL}/open/yolink/token"
API_URL = f"{API_BASE_URL}/open/yolink/v2/api"

# curl -X POST -d "grant_type=client_credentials&client_id=ua_01B5C47165D547DDB157CD5E3E6DA200&client_secret=sec_v1_uXGDjJ+3Xr4CBBOwW6/e3g==" https://api.yosmart.com/open/yolink/token

token = None
action = None
dataPacket = None
headers = {
    'Accept': 'application/json'
}

# First, get the token
dataPacket = {
    'grant_type': 'client_credentials',
    'client_id': UAID,
    'client_secret': SECRET_KEY
}
response = requests.post(f"{API_TOKEN_URL}", data=dataPacket, headers=headers)
js = response.json()
if 'state' in js and js['state'] == 'error':
    print(js['msg'])
elif 'code' in js and js['code'] == '010103':  # Authorization not valid!
    print(js['desc'])
elif 'access_token' in js:
    token = js['access_token']
else:
    print("ERROR: Unable to get access token")

if token:
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    dataPacket = {
        'method': "Home.getDeviceList",
        'time': str(int(time.time()*1000))
    }
    response = requests.post(f"{API_URL}", data=json.dumps(dataPacket), headers=headers)
    js = response.json()
    if 'data' in js:
        devices = [x for x in js['data']['devices'] if x['type'] == 'SpeakerHub']
        if len(devices) <= 0:
            print("ERROR: No Speaker Hubs")
        else:
            dataPacket = {
                'method': "SpeakerHub.playAudio",
                'targetDevice': devices[0]['deviceId'],
                'token': devices[0]['token'],
                'params.tone': 'Warn',
                'params.message': 'Watson, come here, I need you.',
                'params.volume': 10,
                'params.repeat': 1,
                'time': str(int(time.time()*1000))
            }
            response = requests.post(f"{API_URL}", data=json.dumps(dataPacket), headers=headers)
            js = response.json()

            # Errors:
            if 'code' in js:
                if js['code'] == '000000':
                    print("SUCCESS!")
                elif js['code'] in ['000201', '000103']: # Cannot connect, token not valid
                    print(f"ERROR: {js['desc']}")

    else:
        print("ERROR: No data in device list?")
    x = 5
