import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

EMAIL = os.environ["EMAIL_USER"]
PASSWORD = os.environ["EMAIL_PASSWORD"]

with open(
    "output/newsletter.html",
    "r",
    encoding="utf8"
) as f:
    html = f.read()

# Create email
msg = MIMEMultipart()

msg["Subject"] = "☕ STW Coffee Club Daily"
msg["From"] = EMAIL
msg["To"] = EMAIL

# HTML body
msg.attach(
    MIMEText(html, "html")
)

# PNG attachment
with open(
    "output/newsletter.png",
    "rb"
) as f:

    part = MIMEBase(
        "application",
        "octet-stream"
    )

    part.set_payload(
        f.read()
    )

encoders.encode_base64(part)

part.add_header(
    "Content-Disposition",
    "attachment; filename=newsletter.png"
)

msg.attach(part)

# Send
server = smtplib.SMTP(
    "smtp.gmail.com",
    587
)

server.starttls()

server.login(
    EMAIL,
    PASSWORD
)

server.sendmail(
    EMAIL,
    EMAIL,
    msg.as_string()
)

server.quit()

print("✅ Email sent")
