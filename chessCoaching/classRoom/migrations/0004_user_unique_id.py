# Generated by Django 4.2.7 on 2024-02-19 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classRoom', '0003_remove_user_email_remove_user_password_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('id',), name='unique_id'),
        ),
    ]