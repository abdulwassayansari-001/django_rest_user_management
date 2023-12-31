# Generated by Django 4.2.7 on 2023-12-01 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_child_email_child_is_active_child_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='child',
            name='password',
            field=models.CharField(default=1, max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]
