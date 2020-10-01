import fortnitepy
import asyncio
import os
import json
import requests

instances = {}
filename = './device_auths.json'
credentials = {
    "email": "pass",
    "email2": "pass2"
}

def get_device_auth_details():
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open(filename, 'w') as fp:
        json.dump(existing, fp)

async def event_sub_device_auth_generate(details, email):
    store_device_auth_details(email, details)

async def event_sub_ready(client):
    instances[client.user.id] = client         

def Claimer():
    
    for client in clients:

        with requests.Session() as session:

            try: 
                print("[" + client.user.display_name + "] >> Claiming the daily reward...")

                data = {}
                res = session.post(
                    f"https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{client.user.id}/client/ClaimLoginReward?profileId=campaign",
                    headers={
                        "Authorization": f"{client.auth.authorization}",
                        "Content-Type": "application/json"
                    },
                    data=json.dumps(data)
                )

                if(res.status_code == 200):
                    print("[" + client.user.display_name + "] >> Claimed successfully the daily reward!")
                
                else:
                    print("[" + client.user.display_name + "] >> Error claiming the daily reward!")

            except:
                print("[" + client.user.display_name + "] >> Something went wrong claiming the daily reward!")
                pass

clients = []

for email, password in credentials.items():

    device_auths = get_device_auth_details().get(email, {})
    authentication = fortnitepy.AdvancedAuth(
        email=email,
        password=password,
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        **device_auths
    )

    client = fortnitepy.Client(auth=authentication)

    client.add_event_handler('device_auth_generate', event_sub_device_auth_generate)

    clients.append(client)

fortnitepy.run_multiple(
    clients,
    ready_callback=event_sub_ready,
    all_ready_callback=lambda: Claimer()
)