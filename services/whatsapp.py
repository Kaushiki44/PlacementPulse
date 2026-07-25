from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(account_sid, auth_token)

def send_whatsapp(phone, message):
    print("Sending to:", phone)
    print("Message length:", len(message))
    print("First 200 chars:")
    print(message[:200])
    msg = client.messages.create(
        from_=twilio_number,
        to=f"whatsapp:{phone}",
        body=message
    )

    print("Message SID:", msg.sid)