# Generated by Django 2.2.5 on 2019-09-18 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_phone', '0003_auto_20190918_0827'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_phone',
            old_name='userWantsToReceiveWeatherSMS',
            new_name='wantsToReceiveWeatherSMS',
        ),
    ]