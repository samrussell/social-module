from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import render
from django.http import HttpResponseRedirect

import logging
logger = logging.getLogger(__name__)

from .forms import CustomUserCreationForm, CustomUserChangeForm, EmailTemplateSelectForm
from emails.models import EmailTemplate

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_filter = UserAdmin.list_filter + ('notification_event_digest', 'notification_group_digest', 'notification_post_replies')

    list_display = [
        'email',
        'username',
        'first_name',
        'last_name',
        'notification_event_digest',
        'notification_group_digest',
        'notification_post_replies',
    ]
    fieldsets = (
            (None, {'fields': ('username', 'password')}),
            ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
            ('Notifications', {'fields': (
                        'notification_event_digest',
                        'notification_group_digest',
                        'notification_post_replies')}),
            ('Permissions',
            {'fields': ('is_active',
                        'is_staff',
                        'is_superuser',
                        'groups',
                        'user_permissions')}),
            ('Important dates', {'fields': ('last_login', 'date_joined')}))

    actions = ['send_email']

    @admin.action(description='Send test email')
    def send_email(self, request, queryset):
        logger.error("send email")
        if 'apply' in request.POST:
            logger.error("Form sent")
            template = EmailTemplate.objects.get(pk=request.POST['template'])
            self.message_user(request, "Sending template %s" % template.title)
            for user in queryset:
                logger.error("User type: %s" % type(user))
                logger.error("Template: %s" % template)
                template.create_email(user)
            return HttpResponseRedirect(request.get_full_path())

        form = EmailTemplateSelectForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        return render(request, 'admin/send_email.html', {'items': queryset, 'form': form})


admin.site.register(CustomUser, CustomUserAdmin)