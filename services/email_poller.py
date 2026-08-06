from services.gmail import connect_gmail, mark_as_read
from services.subscriber import get_all_subscribers
from services.whatsapp import send_whatsapp
from services.email_filter import is_placement_email

import time
import logging

logger = logging.getLogger(__name__)


def poll_emails():

    while True:

        try:

            unread_emails = connect_gmail()

            if unread_emails:

                subscribers = get_all_subscribers()

                for email_data in unread_emails:

                    if not is_placement_email(email_data):
                        logger.info(f"Skipped non-placement email: {email_data['subject']}")
                        mark_as_read(email_data["id"])
                        continue

                    logger.info(f"Placement email detected: {email_data['subject']}")

                    for subscriber in subscribers:

                        message = (
                            f"📢 {email_data['subject']}\n\n"
                            f"{email_data['body'][:1200]}"
                        )

                        send_whatsapp(
                            subscriber["phone"],
                            message
                        )

                    mark_as_read(email_data["id"])

        except Exception as e:
            logger.error(f"Poller error: {e}")

        logger.info("Checking again in 30 seconds...")
        time.sleep(30)