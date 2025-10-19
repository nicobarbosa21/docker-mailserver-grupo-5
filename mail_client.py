import email
import imaplib
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from typing import List, Tuple

SMTP_SERVER = "localhost"
SMTP_PORT = 1587
IMAP_SERVER = "localhost"
IMAP_PORT = 1143

SENDER_EMAIL = "nico@local.test"
SENDER_PASSWORD = "pass123"

RECEIVER_EMAIL = "facu@local.test"
RECEIVER_PASSWORD = "pass456"


def send_email(
    subject: str,
    body: str,
    sender: str = SENDER_EMAIL,
    recipient: str = RECEIVER_EMAIL,
    password: str = SENDER_PASSWORD,
    smtp_server: str = SMTP_SERVER,
    smtp_port: int = SMTP_PORT,
) -> None:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient
    message["Date"] = formatdate(localtime=True)
    message["Message-ID"] = make_msgid(domain="mail.local.test")
    message.set_content(body)

    context = ssl._create_unverified_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=context)
        server.login(sender, password)
        server.send_message(message)


def fetch_recent_messages(
    limit: int = 10,
    recipient: str = RECEIVER_EMAIL,
    password: str = RECEIVER_PASSWORD,
    imap_server: str = IMAP_SERVER,
    imap_port: int = IMAP_PORT,
) -> List[Tuple[str, str, str]]:
    context = ssl._create_unverified_context()
    mail = imaplib.IMAP4(imap_server, imap_port)
    mail.starttls(ssl_context=context)
    mail.login(recipient, password)
    try:
        mail.select("INBOX")
        status, data = mail.search(None, "ALL")
        if status != "OK" or not data or not data[0]:
            return []

        mail_ids = data[0].split()
        recent_ids = mail_ids[-limit:]
        messages: List[Tuple[str, str, str]] = []

        for msg_id in reversed(recent_ids):
            status, msg_data = mail.fetch(msg_id, "(RFC822)")
            if status != "OK":
                continue
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    body = _extract_text_body(msg)
                    messages.append(
                        (
                            msg.get("Date", ""),
                            msg.get("From", ""),
                            body,
                        )
                    )
        return messages
    finally:
        mail.logout()


def _extract_text_body(message: email.message.Message) -> str:
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode(part.get_content_charset() or "utf-8", errors="replace")
        return ""
    payload = message.get_payload(decode=True)
    if not payload:
        return ""
    return payload.decode(message.get_content_charset() or "utf-8", errors="replace")


__all__ = [
    "send_email",
    "fetch_recent_messages",
    "SENDER_EMAIL",
    "RECEIVER_EMAIL",
]
