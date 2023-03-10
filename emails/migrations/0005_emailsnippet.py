# Generated by Django 4.0.8 on 2023-03-08 07:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('emails', '0004_emailtemplate_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSnippet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_content', models.TextField()),
                ('rich_content', models.TextField()),
                ('source', models.CharField(choices=[('US', 'Unsent'), ('SE', 'Sent')], default='US', max_length=2)),
                ('status', models.CharField(choices=[('RE', 'Reply'), ('ED', 'Event Digest'), ('GD', 'Group Digest')], default='US', max_length=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snippets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]