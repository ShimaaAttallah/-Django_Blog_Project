from django.core.mail import send_mail
from django.conf import settings
import threading
from django.core.mail import EmailMessage


def send_forget_password_mail(email, token):
    subject = 'change in your category list'
    message = str(token)
    email_from = settings.EMAIL_HOST_USER
    recipitient_list = [email]
    send_mail(subject, message, email_from, recipitient_list)
    return True


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list, sender):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.sender = sender
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content,
                           self.sender, self.recipient_list)
        msg.content_subtype = 'html'
        msg.send()


def send_html_mail(subject, html_content):
    EmailThread(subject, html_content, ['aaloub15@gmail.com'],
                'testdjango55@gmail.com').start()
