# Generated by Django 5.0.2 on 2024-03-06 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classRoom', '0009_chapter_page_userpageactivity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='id',
        ),
        migrations.RemoveField(
            model_name='page',
            name='id',
        ),
        migrations.RemoveField(
            model_name='userpageactivity',
            name='id',
        ),
        migrations.AddField(
            model_name='chapter',
            name='chapter_id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='page_id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userpageactivity',
            name='pageactivity_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]