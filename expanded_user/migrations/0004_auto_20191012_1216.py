# Generated by Django 2.2.5 on 2019-10-12 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expanded_user', '0003_auto_20190919_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='custom_user',
            name='userLatitude',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='custom_user',
            name='userLongitude',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
