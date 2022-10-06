import smtplib, ssl
from email.mime.text import MIMEText

from passwords import rambler
def send_mail(message):
    sender = 'sb.robot@ro.ru'
    receivers = ['komaroff.ilya.s@gmail.com']

    port = 465
    user = 'sb.robot@ro.ru'
    password = rambler

    msg = MIMEText(message)

    msg['Subject'] = 'Тестовое письмо'
    msg['From'] = 'sb.robot@ro.ru'
    msg['To'] = 'komaroff.ilya.s@gmail.com'

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.rambler.ru', port, context=context) as server:

     server.login(user, password)
     server.sendmail(sender, receivers, msg.as_string())
     print('mail successfully sent')

send_mail("привет")