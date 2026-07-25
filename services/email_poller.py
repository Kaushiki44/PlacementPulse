from services.gmail import connect_gmail
from services.subscriber import get_all_subscribers
from services.whatsapp import send_whatsapp


def poll_emails():

    email = connect_gmail()

    if email:
        subscribers = get_all_subscribers()

        for subscriber in subscribers:
            message = (
                f"📢 {email['subject']}\n\n"
                f"{email['body'][:1200]}"
            )

            send_whatsapp(subscriber["phone"], message)