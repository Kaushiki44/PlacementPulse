import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def connect_gmail():
    try:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, EMAIL_PASSWORD)

        print("✅ Gmail login successful")

        # Select Inbox
        mail.select("INBOX")

        # Search unread emails
        status, messages = mail.search(None, "UNSEEN")

        if status != "OK":
            print("❌ Failed to search emails.")
            return None

        # No unread emails
        if messages[0] == b"":
            print("📭 No unread emails.")
            return None

        # Latest unread email ID
        ids = messages[0].split()
        latest = ids[-1]

        print("Unread Email IDs:", ids)
        print("Latest Email ID:", latest)

        # Fetch email
        status, data = mail.fetch(latest, "(RFC822)")

        if status != "OK":
            print("❌ Failed to fetch email.")
            return mail

        msg = email.message_from_bytes(data[0][1])

        # Decode Subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8", errors="ignore")

        sender = msg["From"]

        body = ""

        if msg.is_multipart():
            for part in msg.walk():

                content_type = part.get_content_type()
                disposition = str(part.get("Content-Disposition"))

                if (
                    content_type == "text/plain"
                    and "attachment" not in disposition.lower()
                ):
                    body = part.get_payload(decode=True).decode(
                        errors="ignore"
                    )
                    break

        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")


        return {
            "subject": subject,
            "from": sender,
            "body": body
        }

    except Exception as e:
        print("❌ Gmail login failed")
        print(e)
        return None