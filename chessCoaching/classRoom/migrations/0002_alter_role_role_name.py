# Generated by Django 4.2.7 on 2024-02-27 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classRoom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='role_name',
            field=models.CharField(max_length=255),
        ),
    ]