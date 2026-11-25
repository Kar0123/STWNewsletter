import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL = os.environ["EMAIL_USER"]
PASSWORD = os.environ["EMAIL_PASSWORD"]

with open(
    "output/newsletter.html",
    "r",
    encoding="utf8"
) as f:
    html = f.read()

msg = MIMEMultipart("alternative")

msg["Subject"] = "☕ STW Coffee Club Daily"
msg["From"] = EMAIL
msg["To"] = EMAIL

msg.attach(
    MIMEText(html, "html")
)

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