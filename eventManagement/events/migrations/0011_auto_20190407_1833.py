# Generated by Django 2.1.7 on 2019-04-07 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_eventreq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='venue',
            field=models.CharField(max_length=100),
        ),
    ]
