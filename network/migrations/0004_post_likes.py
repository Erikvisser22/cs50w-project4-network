# Generated by Django 4.0.2 on 2022-02-09 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_post_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
