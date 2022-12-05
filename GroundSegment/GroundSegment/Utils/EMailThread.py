'''
Created on 27 de set. de 2016

@author: pabli
'''

import threading

from django.conf import settings
from django.core.mail import send_mail

class EmailThread(threading.Thread):
    def __init__(self, subject, body, recipients):
        self.subject = subject
        self.recipients = recipients
        self.body = body
        threading.Thread.__init__(self)

    def run (self):
        """
        msg = EmailMessage(self.subject, self.html_content, EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        msg.send()
        """
        try:
            send_mail(self.subject, self.body, settings.EMAIL_HOST_USER, self.recipients, fail_silently=False)
        except Exception as ex:
            raise ex

    