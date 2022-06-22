from passwords import google
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(message):
    sender = 'komaroff.ilya.s@gmail.com'
    password = google
    server = smtplib.SMTP('smtp.rambler.ru', 465)
    server.starttls()
    try:
        server.login(sender, password)
        server.sendmail(sender,'komaroff.ilya.s@gmail.com', message)
        print('Сообщение отправлено')
    except Exception as _ex:
        return f'error {_ex}'


def main():
    # message = "test"
    send_email('message')

if __name__ == "__main__":
    main()