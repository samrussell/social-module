# Generated by Django 4.0.8 on 2023-02-22 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_sentemail_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtemplate',
            name='notification_event_digest',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='notification_group_digest',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='notification_post_replies',
            field=models.BooleanField(default=False),
        ),
    ]
