# Generated by Django 3.2.5 on 2021-08-22 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_alter_post_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
