from fastapi import FastAPI, HTTPException, Form
from models import Student
import threading
import logging
from fastapi.responses import Response

from twilio.twiml.messaging_response import MessagingResponse

from services.email_poller import poll_emails
from services.whatsapp import send_whatsapp
from services.subscriber import (
    add_subscriber,
    remove_subscriber,
    get_all_subscribers,
)

import logger

logger = logging.getLogger(__name__)

app = FastAPI()


@app.on_event("startup")
def start_email_poller():
    thread = threading.Thread(target=poll_emails, daemon=True)
    thread.start()


@app.post("/subscribe")
def subscribe(student: Student):

    success = add_subscriber(student.phone)

    if success:
        logger.info(f"Subscriber added: {student.phone}")
        return {
            "message": "Subscribed successfully!"
        }

    logger.warning(f"Subscriber already exists: {student.phone}")

    raise HTTPException(
        status_code=409,
        detail="Phone number already subscribed!"
    )


@app.get("/subscribers")
def get_subscribers():
    return get_all_subscribers()


@app.delete("/unsubscribe/{phone}", status_code=204)
def unsubscribe(phone: str):

    if remove_subscriber(phone):
        logger.info(f"Subscriber removed: {phone}")
        return

    logger.warning(f"Subscriber not found: {phone}")

    raise HTTPException(
        status_code=404,
        detail="Subscriber not found."
    )


@app.post("/webhook")
def webhook(
    From: str = Form(...),
    Body: str = Form(...)
):

    logger.info(f"Incoming WhatsApp message from {From}")
    logger.info(f"Message: {Body}")

    # Extract phone number
    phone = From.replace("whatsapp:", "")

    # Normalize message
    message = Body.strip().lower()

    response = MessagingResponse()

    # ---------------- SUBSCRIBE ----------------
    if message in ["hi", "hello", "subscribe", "start"]:

        if add_subscriber(phone):
            logger.info(f"Subscribed via WhatsApp: {phone}")
            response.message("🎉 You have been subscribed!")

        else:
            logger.warning(f"Already subscribed: {phone}")
            response.message("⚠️ You're already subscribed!")

    # ---------------- UNSUBSCRIBE ----------------
    elif message in ["stop", "unsubscribe"]:

        if remove_subscriber(phone):
            logger.info(f"Unsubscribed via WhatsApp: {phone}")
            response.message(
                "✅ You have been unsubscribed."
            )

        else:
            logger.warning(f"Unsubscribe requested for non-subscriber: {phone}")
            response.message(
                "⚠️ You are not subscribed."
            )

    # ---------------- UNKNOWN COMMAND ----------------
    else:

        logger.info(f"Unknown command from {phone}: {message}")

        response.message(
            "👋 Welcome to PlacementPulse!\n\n"
            "Available commands:\n"
            "• HI - Subscribe\n"
            "• STOP - Unsubscribe"
        )

    twiml = str(response)

    logger.info(f"Generated TwiML: {twiml}")

    return Response(
        content=twiml,
        media_type="application/xml"
    )


@app.get("/test-whatsapp")
def test_whatsapp():

    logger.info("Testing WhatsApp integration")

    send_whatsapp(
        "+918957042510",
        "Hello from PlacementPulse 🚀"
    )

    return {
        "message": "WhatsApp message sent!"
    }