from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser
from forum.models import Comment

import requests
import json

# Create your models here.

class SendEmailCommentJob(models.Model):
    CREATED = 'CR'
    IN_PROGRESS = 'IP'
    COMPLETED = 'CO'

    EMAIL_COMMENT_JOB_STATUSES = [
        (CREATED, 'Created'),
        (IN_PROGRESS, 'In progress'),
        (COMPLETED, 'Completed'),
    ]

    status = models.CharField(max_length=2, choices=EMAIL_COMMENT_JOB_STATUSES, default=CREATED)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def run(self):
        for snippet in self.snippets.all():
            # build SentEmail from snippet
            sent_email = snippet.build_email()
            sent_email.job = self
            sent_email.save()
        return True
        


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
    job = models.ForeignKey(SendEmailCommentJob, on_delete=models.CASCADE, related_name='sent_emails', blank=True, null=True)

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
    INACTIVE = 'IA'
    ACTIVE = 'AC'

    EMAIL_TEMPLATE_STATUSES = [
        (INACTIVE, 'Inactive'),
        (ACTIVE, 'Active'),
    ]

    title = models.CharField(max_length=255)
    template_body = models.TextField()
    notification_event_digest = models.BooleanField(default=False)
    notification_group_digest = models.BooleanField(default=False)
    notification_post_replies = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=EMAIL_TEMPLATE_STATUSES, default=INACTIVE)

    def create_email(self, user):
        email = SentEmail(from_address='develop@thomasmoore.me', 
                          to_address=user.email,
                          subject=self.title,
                          body=self.template_body
                          )
        email.save()

    def __str__(self):
        return self.title

class EmailCommentSnippet(models.Model):
    UNSENT = 'US'
    SENT = 'SE'

    EMAIL_SNIPPET_STATUSES = [
        (UNSENT, 'Unsent'),
        (SENT, 'Sent'),
    ]

    text_content = models.TextField()
    rich_content = models.TextField()
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='snippets')
    source = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='snippets')
    status = models.CharField(max_length=2, choices=EMAIL_SNIPPET_STATUSES, default=UNSENT)
    job = models.ForeignKey(SendEmailCommentJob, on_delete=models.CASCADE, related_name='snippets', blank=True, null=True)

    def build_email(self):
        if self.status != self.UNSENT:
            raise Exception('Tried to send mail but status is %s' % self.status)
        
        email = SentEmail(from_address='develop@thomasmoore.me', 
                          to_address=self.user.email,
                          subject="Reply to post %s" % self.source.post.title,
                          body=self.text_content
                          )
        email.save()
        self.status = self.SENT
        self.save()

        return email

@receiver(post_save, sender=Comment)
def create_comment_snippet(sender, instance, **kwargs):
    snippet = EmailCommentSnippet.objects.create(
        text_content=instance.body,
        rich_content=instance.body,
        user=instance.author,
        source=instance
    )
    snippet.save()

