from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import Form, BooleanField, CheckboxInput, ModelChoiceField, CharField, MultipleHiddenInput
from emails.models import EmailTemplate


CustomUser = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username',)

class NotificationsForm(Form):
    event_switch = BooleanField(required=False, widget=CheckboxInput(attrs={'id': 'event_switch', 'for': 'event_switch', 'class': 'form-check-input'}))
    group_switch = BooleanField(required=False, widget=CheckboxInput(attrs={'id': 'group_switch', 'for': 'group_switch', 'class': 'form-check-input'}))
    reply_switch = BooleanField(required=False, widget=CheckboxInput(attrs={'id': 'reply_switch', 'for': 'reply_switch', 'class': 'form-check-input'}))

class EmailTemplateSelectForm(Form):
    _selected_action = CharField(widget=MultipleHiddenInput)
    template = ModelChoiceField(queryset=EmailTemplate.objects.filter(status=EmailTemplate.ACTIVE))