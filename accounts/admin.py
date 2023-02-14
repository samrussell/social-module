from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


from .forms import CustomUserCreationForm, CustomUserChangeForm


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

    @admin.action(description='Send email')
    def send_email(self, request, queryset):
        self.message_user(request, "Sending email to %s" % list(queryset))


admin.site.register(CustomUser, CustomUserAdmin)