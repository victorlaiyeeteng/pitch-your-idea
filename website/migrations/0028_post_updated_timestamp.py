# Generated by Django 3.2.5 on 2021-10-31 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0027_auto_20211029_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='updated_timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
