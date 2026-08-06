import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re
import logging

load_dotenv()
logger = logging.getLogger(__name__)

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

        logger.info("Gmail login successful")

        # Select Inbox
        mail.select("INBOX")

        # Search unread emails
        status, messages = mail.search(None, "UNSEEN")

        if status != "OK":
            logger.error("Failed to search emails.")
            return None

        if messages[0] == b"":
            logger.info("No unread emails.")
            return None

        ids = messages[0].split()

        logger.info(f"Unread emails found: {len(ids)}")

        # Fetch latest unread email
        emails = []

        for email_id in ids:

            status, data = mail.fetch(email_id, "(RFC822)")

            if status != "OK":
                logger.warning(f"Failed to fetch email {email_id}. Skipping.")
                continue

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
                
            emails.append({
                "id": email_id,
                "subject": subject,
                "from": sender,
                "body": body,
            })

        mail.logout()
        return emails
        

    except Exception as e:
        logger.error(f"Gmail login failed: {e}")
        return None


def mark_as_read(email_id):
    try:

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, EMAIL_PASSWORD)
        mail.select("INBOX")

        mail.store(email_id, "+FLAGS", "\\Seen")
        mail.logout()

        logger.info(f"Marked email {email_id} as read.")

    except Exception as e:
        logger.error(f"Failed to mark email as read: {e}")