# Generated by Django 4.2.9 on 2024-01-10 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='id',
            new_name='student_id',
        ),
    ]