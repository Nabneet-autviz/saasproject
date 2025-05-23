# Generated by Django 4.2.7 on 2024-06-27 13:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0003_questionchoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
