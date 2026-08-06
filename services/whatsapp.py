from twilio.rest import Client
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(account_sid, auth_token)


def send_whatsapp(phone, message):
    try:
        logger.info(f"Sending WhatsApp to {phone}")

        msg = client.messages.create(
            from_=twilio_number,
            to=f"whatsapp:{phone}",
            body=message
        )

        logger.info(f"Message sent successfully. SID: {msg.sid}")

    except Exception as e:
        logger.error(f"Failed to send WhatsApp to {phone}: {e}")