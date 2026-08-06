from services.gmail import connect_gmail
from services.subscriber import get_all_subscribers
from services.whatsapp import send_whatsapp
from services.email_filter import is_placement_email

def poll_emails():

    email_data  = connect_gmail()

    if not email_data :
        return

    if not is_placement_email(email_data ):
        print("📭 Non-placement email. Skipping...")
        return

    print("✅ Placement email detected.")

    subscribers = get_all_subscribers()

    for subscriber in subscribers:
        message = (
            f"📢 {email_data['subject']}\n\n"
            f"{email_data['body'][:1200]}"
        )

        send_whatsapp(subscriber["phone"], message)