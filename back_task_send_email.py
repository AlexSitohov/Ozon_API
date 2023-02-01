import os
import smtplib
from email.message import EmailMessage
from config import SMTP_USER, SMTP_PASSWORD

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587

SMTP_USER = SMTP_USER
SMTP_PASSWORD = SMTP_PASSWORD


def send_email(user, order):
    username = user.username
    user_email = user.email

    email = create_email_template(username, user_email, order)

    smtp_server = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
    smtp_server.starttls()
    smtp_server.login(SMTP_USER, SMTP_PASSWORD)
    smtp_server.send_message(email)


def create_email_template(username, user_email, order):
    email = EmailMessage()
    email['Subject'] = f'Здравствуйте {username}'
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        f'''
        <div>
        <h1 style="color: red;">Здравствуйте {username}. 😊</h1>
        <h2>Статус вашего заказа: {order.id} обновлен на {order.status} </h2>
        <img src="https://sun9-55.userapi.com/impg/UI7iQX4y_Hi0w-EDdWasIUQi_LQBxw7uAfr5Mg/PZjYAOik45I.jpg?size=2560x1440&quality=96&sign=3aea9c6b509c6c9c0cacbcfaed248d82&type=album" width="600">
        </div>
        ''',
        subtype='html'
    )
    return email
