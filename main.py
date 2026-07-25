from fastapi import FastAPI, HTTPException, Form
from models import Student
import pymysql
import threading
from twilio.twiml.messaging_response import MessagingResponse
from services.email_poller import poll_emails
from services.whatsapp import send_whatsapp
from services.subscriber import (
    add_subscriber,
    remove_subscriber,
    get_all_subscribers,
)

app = FastAPI()

@app.on_event("startup")
def start_email_poller():
    thread = threading.Thread(target=poll_emails, daemon=True)
    thread.start()


@app.post("/subscribe")
def subscribe(student: Student):

    success = add_subscriber(student.phone)

    if success:
        return {
            "message": "Subscribed successfully!"
        }

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
        return

    raise HTTPException(
        status_code=404,
        detail="Subscriber not found."
    )


@app.post("/webhook")
def webhook(
    From: str = Form(...),
    Body: str = Form(...)
):

    print("From:", From)
    print("Body:", Body)

    # Extract phone number
    phone = From.replace("whatsapp:", "")

    # Normalize message
    message = Body.strip().lower()

    response = MessagingResponse()

    # ---------------- SUBSCRIBE ----------------
    if message in ["hi", "hello", "subscribe", "start"]:

        if add_subscriber(phone):
            response.message("🎉 You have been subscribed!")

        else:
            response.message("⚠️ You're already subscribed!")


    # ---------------- UNSUBSCRIBE ----------------
    elif message in ["stop", "unsubscribe"]:

        if remove_subscriber(phone):

            response.message(
                "✅ You have been unsubscribed."
            )

        else:

            response.message(
                "⚠️ You are not subscribed."
            )


        # ---------------- UNKNOWN COMMAND ----------------
    else:

        response.message(
            "👋 Welcome to PlacementPulse!\n\n"
            "Available commands:\n"
            "• HI - Subscribe\n"
            "• STOP - Unsubscribe"
        )

    # return str(response)
    twiml = str(response)

    print("========== TWIML ==========")
    print(twiml)
    print("===========================")

    return twiml


@app.get("/test-whatsapp")
def test_whatsapp():
    send_whatsapp(
        "+918957042510",
        "Hello from PlacementPulse 🚀"
    )

    return {
        "message": "WhatsApp message sent!"
    }