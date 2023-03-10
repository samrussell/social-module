from django.contrib import admin, messages

from .models import SentEmail, EmailTemplate, EmailCommentSnippet, SendEmailCommentJob

# Register your models here.

@admin.register(SentEmail)
class SentEmailAdmin(admin.ModelAdmin):
    actions = ['send_email']
    list_display = ['from_address', 'to_address', 'subject', 'status']

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

@admin.register(EmailCommentSnippet)
class EmailCommentSnippetAdmin(admin.ModelAdmin):
    list_display = ['user', 'source', 'status']

@admin.register(SendEmailCommentJob)
class SendEmailCommentJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'status']
    actions = ['add_all_new_snippets', 'create_emails']

    @admin.action(description='Add all new snippets')
    def add_all_new_snippets(self, request, queryset):
        pass

    @admin.action(description='Create emails from snippets')
    def create_emails(self, request, queryset):
        for job in queryset:
            try:
                result = job.run()
                self.message_user(request, "SentEmail objects created")
            except Exception as e:
                self.message_user(request, 'ERROR: job %d failed: %s' % (job.id, e), level=messages.ERROR)

