# Generated by Django 2.2.5 on 2019-09-19 14:37

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('expanded_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custom_user',
            name='userCountry',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]