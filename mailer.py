import smtplib
from email.message import EmailMessage
from models import Order
from typing import List

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_FROM = "adrian.jurisic.20@size.ba"
EMAIL_TO = "adrianjurisic1601@gmail.com"
EMAIL_PASSWORD = "lntv rliv hmzm rwxq"

def format_order(order: Order) -> str:
    lines = [f"Nova narudžba #{order.id} od {order.kupac.ime} {order.kupac.prezime}",
             f"Adresa: {order.kupac.adresa}",
             f"Telefon: {order.kupac.telefon}",
             f"Email: {order.kupac.email or '-'}",
             f"Datum: {order.kreirano.strftime('%Y-%m-%d %H:%M')}",
             "\nStavke:"]
    for item in order.stavke:
        lines.append(f"- Proizvod #{item.product_id}, količina: {item.quantity}")
    return "\n".join(lines)

def send_order_email(order: Order):
    try:
        msg = EmailMessage()
        msg["Subject"] = f"Nova narudžba #{order.id}"
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO
        msg.set_content(format_order(order))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email poslan adminu!")
    except Exception as e:
        print("Nije moguće poslati email:", e)
