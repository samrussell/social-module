from django.db import models

import requests
import json

# Create your models here.

class SentEmail(models.Model):
    UNSENT = 'US'
    SUCCESS = 'OK'
    FAILURE = 'FL'

    SENT_EMAIL_CHOICES = [
        (UNSENT, 'Unsent'),
        (SUCCESS, 'Success'),
        (FAILURE, 'Failure')
    ]

    status = models.CharField(max_length=2, choices=SENT_EMAIL_CHOICES, default=UNSENT)
    from_address = models.CharField(max_length=255)
    to_address = models.CharField(max_length=255)
    subject = models.TextField()
    body = models.TextField()

    def send(self):
        if self.status != self.UNSENT:
            raise Exception('Tried to send mail but status is %s' % self.status)
        
        url = "https://api.postmarkapp.com/email"

        payload = json.dumps({
        "From": self.from_address,
        "To": self.to_address,
        "Subject": self.subject,
        "TextBody": self.body,
        "HtmlBody": self.body,
        "MessageStream": "outbound"
        })
        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Postmark-Server-Token': 'POSTMARK_API_TEST'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        # assume success

        self.status = self.SUCCESS

        self.save()

        return response

class EmailTemplate(models.Model):
    title = models.CharField(max_length=255)
    template_body = models.TextField()
