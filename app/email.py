from flask import current_app
from flask_mail import Message
from app import mail
from threading import Thread

# regarding 'with' statements in this...context:
# https://docs.python.org/3/reference/compound_stmts.html#with
# TODO understand how 'with' is used in more detail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    #mail.send(msg)
    Thread(target=send_async_email, \
        args=(current_app._get_current_object(), msg)).start()

