from email.utils import parseaddr

PLACEMENT_SENDERS = [
    "placement@jssaten.ac.in",
    "tnp@jssaten.ac.in",
    "placements@jssuninoida.edu.in",
    "kaushikiofficial44@gmail.com"
]

def is_placement_email(email_data):
    _, sender_email = parseaddr(email_data["from"])

    sender_email = sender_email.lower()

    return sender_email in PLACEMENT_SENDERS