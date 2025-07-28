import smtplib
from email.message import EmailMessage
from models import Order
from database import get_product_by_id

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_FROM = "adrian.jurisic.20@size.ba"
EMAIL_TO = "adrianjurisic1601@gmail.com"
EMAIL_PASSWORD = "lntv rliv hmzm rwxq"

def format_order(order: Order) -> str:
    lines = [
        f"📦 NOVA NARUDŽBA #{order.id}",
        "-" * 40,
        f"👤 Kupac: {order.kupac.ime} {order.kupac.prezime}",
        f"🏠 Adresa: {order.kupac.adresa}",
        f"📞 Telefon: {order.kupac.telefon}",
        f"📧 Email: {order.kupac.email or '-'}",
        f"📅 Datum: {order.kreirano.strftime('%Y-%m-%d %H:%M')}",
        "",
        "🛒 Stavke u narudžbi:"
    ]

    ukupno = 0.0

    for item in order.stavke:
        product = get_product_by_id(item.product_id)
        if product:
            item_total = product.price * item.quantity
            ukupno += item_total
            lines.append(
                f"• {product.name} — {item.quantity} x {product.price:.2f} KM = {item_total:.2f} KM"
            )
        else:
            lines.append(
                f"• Nepoznat proizvod (ID: {item.product_id}) — količina: {item.quantity}"
            )

    lines.append("")
    lines.append(f"💰 Ukupno za platiti: {ukupno:.2f} KM")
    lines.append("-" * 40)
    lines.append("💻 Sistem: Webshop by Adrian")

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