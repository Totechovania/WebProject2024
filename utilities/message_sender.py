import smtplib
from random import randint


def send_email(message, recipient):
    sender = 'mrromashok@gmail.com'
    password = 'bxll ylfm jvrk vegm'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(sender, password)
        server.sendmail(sender, recipient, f'Subject: Registration to DeMedia\n\nYour code: {message}')

        return "Message sent successfully!"
    except Exception as er:
        return f'{er}\n Error'


def generate_code():
    return randint(100000, 999999)
