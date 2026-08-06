# 🚀 PlacementPulse

**PlacementPulse** is a FastAPI-based backend application that automatically monitors Gmail for placement emails and instantly forwards only the placement emails to subscribed students via WhatsApp using Twilio.

It eliminates the need to constantly check email by delivering placement notifications directly to students' WhatsApp.


---

## 🏗️ Architecture

```text
                Placement Email
                       │
                       ▼
                Gmail Inbox (IMAP)
                       │
                       ▼
              Background Email Poller
                       │
                       ▼
            Placement Email Filter
                       │
                       ▼
             Subscriber Database
                  (MySQL)
                       │
                       ▼
             Twilio WhatsApp API
                       │
                       ▼
          WhatsApp Notifications
```

---

## 🛠️ Tech Stack

- **Backend:** FastAPI
- **Database:** MySQL
- **Email Processing:** IMAP, BeautifulSoup
- **Messaging:** Twilio WhatsApp Sandbox API
- **Language:** Python
- **Deployment Tunnel (Development):** Cloudflare Tunnel

---

## 📂 Project Structure

```
PlacementPulse/
│
├── services/
│   ├── email_filter.py
│   ├── email_poller.py
│   ├── gmail.py
│   ├── subscriber.py
│   └── whatsapp.py
│
├── main.py
├── database.py
├── models.py
├── logger.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd PlacementPulse
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file:

```env
EMAIL=
EMAIL_PASSWORD=

TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_NUMBER=

DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
```

### 6. Start the server

```bash
uvicorn main:app --reload
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/subscribe` | Subscribe a phone number |
| DELETE | `/unsubscribe/{phone}` | Remove a subscriber |
| GET | `/subscribers` | List all subscribers |
| POST | `/webhook` | Twilio WhatsApp webhook |
| GET | `/test-whatsapp` | Test WhatsApp integration |

---

## 🔄 Workflow

1. Placement email arrives in the monitored Gmail inbox.
2. Background poller checks for unread emails every 30 seconds.
3. Placement emails are identified using sender filtering.
4. Email content is cleaned and formatted.
5. Subscriber phone numbers are fetched from MySQL.
6. Twilio sends WhatsApp notifications.
7. Processed emails are marked as read to prevent duplicate notifications.

---

## 👩‍💻 Author

**Kaushiki Sahu**