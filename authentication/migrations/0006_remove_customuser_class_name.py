# Generated by Django 4.2.7 on 2024-07-10 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_customuser_class_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='class_name',
        ),
    ]
