import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

client = WebClient(token=SLACK_BOT_TOKEN)


def list_channels():
    try:
        response = client.conversations_list()
        channels = response["channels"]
        print("Canaux disponibles :")
        for ch in channels:
            print(f"- #{ch['name']} (id: {ch['id']})")
        return channels
    except SlackApiError as e:
        print(f"Erreur : {e.response['error']}")
        return []


def send_test_message(channel_id: str, text: str):
    try:
        response = client.chat_postMessage(channel=channel_id, text=text)
        print(f"Message envoye dans {channel_id} : {text}")
    except SlackApiError as e:
        print(f"Erreur d'envoi : {e.response['error']}")


if __name__ == "__main__":
    channels = list_channels()

    if channels:
        target_channel = "C0BKKAS56H0"  # #tous-chaimae, ou le bot a ete invite
        send_test_message(target_channel, "Ceci est un message de test de l'agent IA.")
