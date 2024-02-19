# Generated by Django 4.2.7 on 2024-02-19 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classRoom', '0004_user_unique_id'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='user',
            name='unique_id',
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default=0, max_length=254),
            preserve_default=False,
        ),
    ]
