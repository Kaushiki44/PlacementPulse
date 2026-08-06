from services.gmail import connect_gmail
from services.subscriber import get_all_subscribers
from services.whatsapp import send_whatsapp
from services.email_filter import is_placement_email
import time


def poll_emails():

    unread_emails = connect_gmail()

    if not unread_emails:
        return

    subscribers = get_all_subscribers()
    
    for email_data in unread_emails:

        if not is_placement_email(email_data):
            print("📭 Non-placement email. Skipping...")
            continue

        print("✅ Placement email detected.")

        for subscriber in subscribers:

            message = (
                f"📢 {email_data['subject']}\n\n"
                f"{email_data['body'][:1200]}"
            )

            send_whatsapp(
                subscriber["phone"],
                message
            )