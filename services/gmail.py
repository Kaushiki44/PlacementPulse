import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re

load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def clean_email_body(body):
    soup = BeautifulSoup(body, "html.parser")

    text = soup.get_text(separator="\n")

    # Remove extra blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove common invisible Unicode characters
    text = re.sub(
        r"[\u200B-\u200F\u202A-\u202E\u2060\u2066-\u2069\u00A0\u2007\u202F]",
        "",
        text,
    )

    return text.strip()


def is_clean_plain_text(text):
    bad_patterns = [
        "font-family",
        "body,",
        "<html",
        "<div",
        "<table",
        "</",
    ]

    text = text.lower()

    return not any(pattern in text for pattern in bad_patterns)


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

        if messages[0] == b"":
            print("📭 No unread emails.")
            return None

        ids = messages[0].split()
        latest = ids[-1]

        print(f"Unread emails found: {len(ids)}")
        print("Latest Email ID:", latest)

        # Fetch latest unread email
        status, data = mail.fetch(latest, "(RFC822)")

        if status != "OK":
            print("❌ Failed to fetch email.")
            return None

        msg = email.message_from_bytes(data[0][1])

        # Decode subject
        subject, encoding = decode_header(msg["Subject"])[0]

        if isinstance(subject, bytes):
            subject = subject.decode(
                encoding or "utf-8",
                errors="ignore"
            )

        sender = msg["From"]

        body = ""
        plain_body = ""
        html_body = ""

        if msg.is_multipart():

            for part in msg.walk():

                content_type = part.get_content_type()
                disposition = str(part.get("Content-Disposition"))

                if (
                    content_type == "text/plain"
                    and "attachment" not in disposition.lower()
                ):
                    plain_body = part.get_payload(
                        decode=True
                    ).decode(errors="ignore")

                elif (
                    content_type == "text/html"
                    and "attachment" not in disposition.lower()
                ):
                    html_body = part.get_payload(
                        decode=True
                    ).decode(errors="ignore")

            # Decide which version to use
            if plain_body and is_clean_plain_text(plain_body):
                body = plain_body

            elif html_body:
                body = clean_email_body(html_body)

            elif plain_body:
                body = clean_email_body(plain_body)

            else:
                body = ""

        else:
            content_type = msg.get_content_type()

            if content_type == "text/html":
                body = clean_email_body(
                    msg.get_payload(decode=True).decode(
                        errors="ignore"
                    )
                )
            else:
                body = msg.get_payload(
                    decode=True
                ).decode(errors="ignore")

        return {
            "subject": subject,
            "from": sender,
            "body": body,
        }

    except Exception as e:
        print("❌ Gmail login failed")
        print(e)
        return None