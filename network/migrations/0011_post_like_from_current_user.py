# Generated by Django 4.0.2 on 2022-02-12 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_from_current_user',
            field=models.BooleanField(default=False),
        ),
    ]