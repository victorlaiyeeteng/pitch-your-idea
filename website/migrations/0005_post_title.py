# Generated by Django 3.2.5 on 2021-08-11 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_post_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='Untitled', max_length=64),
        ),
    ]
