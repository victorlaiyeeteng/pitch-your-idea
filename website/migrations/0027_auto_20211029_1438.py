# Generated by Django 3.2.5 on 2021-10-29 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0026_alter_post_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='unliked',
        ),
        migrations.DeleteModel(
            name='Unlike',
        ),
    ]
