import os
from fastapi import FastAPI, Request
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Garde en memoire les ids d'evenements deja traites pour eviter les doublons
# (Slack peut renvoyer le meme evenement plusieurs fois)
processed_event_ids = set()


@app.post("/slack/events")
async def slack_events(request: Request):
    payload = await request.json()
    print(f"PAYLOAD RECU: {payload}")
    # 1. Etape de verification d'URL (Slack l'envoie une seule fois a la configuration)
    if payload.get("type") == "url_verification":
        return {"challenge": payload["challenge"]}

    # 2. Evenement reel (message, mention, etc.)
    if payload.get("type") == "event_callback":
        event_id = payload.get("event_id")

        if event_id in processed_event_ids:
            print(f"Evenement {event_id} deja traite, ignore.")
            return {"status": "ok"}

        processed_event_ids.add(event_id)

        event = payload.get("event", {})
        event_type = event.get("type")

        if event_type == "message" and "subtype" not in event:
            user = event.get("user")
            text = event.get("text")
            channel = event.get("channel")
            print(f"[NOUVEAU MESSAGE] canal={channel} user={user} texte={text}")

        elif event_type == "app_mention":
            user = event.get("user")
            text = event.get("text")
            channel = event.get("channel")
            print(f"[MENTION] canal={channel} user={user} texte={text}")

        return {"status": "ok"}

    return {"status": "ignored"}


@app.get("/")
async def health_check():
    return {"status": "running"}
