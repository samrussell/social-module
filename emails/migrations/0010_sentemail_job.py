# Generated by Django 4.0.8 on 2023-03-10 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0009_alter_sendemailcommentjob_completed_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentemail',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_emails', to='emails.sendemailcommentjob'),
        ),
    ]