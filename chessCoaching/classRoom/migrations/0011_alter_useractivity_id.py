# Generated by Django 4.2.7 on 2024-03-06 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classRoom', '0010_alter_useractivity_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]