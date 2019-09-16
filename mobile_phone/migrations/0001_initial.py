# Generated by Django 2.2.5 on 2019-09-16 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='user_phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneCountryCode', models.CharField(max_length=6)),
                ('phoneNumber', models.CharField(max_length=12)),
                ('isMobileValidated', models.BooleanField(default=False)),
                ('sendWeatherSMS', models.BooleanField(default=False)),
                ('timeWeatherSMS', models.CharField(max_length=5)),
                ('userMobilePhone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
