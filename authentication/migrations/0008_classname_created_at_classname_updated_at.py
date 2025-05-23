# Generated by Django 4.2.7 on 2024-07-11 08:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_customuser_class_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='classname',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classname',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
