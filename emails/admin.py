from django.contrib import admin, messages

from .models import SentEmail, EmailTemplate

# Register your models here.

@admin.register(SentEmail)
class SentEmailAdmin(admin.ModelAdmin):
    actions = ['send_email']
    list_display = ['from_address', 'to_address', 'subject']

    @admin.action(description='Send email')
    def send_email(self, request, queryset):
        for sent_email in queryset:
            try:
                response = sent_email.send()
                self.message_user(request, response.text)
            except:
                self.message_user(request, 'ERROR: mail %d has already been sent' % sent_email.id, level=messages.ERROR)

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    actions = ['create_email']
    list_display = ['title', 'status', 'notification_event_digest', 'notification_group_digest', 'notification_post_replies']

    @admin.action(description='Create email')
    def create_email(self, request, queryset):
        for template in queryset:
            try:
                response = template.send()
                self.message_user(request, response.text)
            except:
                self.message_user(request, 'ERROR: mail %d has already been sent' % template.id, level=messages.ERROR)
