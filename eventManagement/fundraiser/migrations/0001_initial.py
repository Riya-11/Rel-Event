# Generated by Django 2.1.7 on 2019-04-19 04:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='eventdeet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.CharField(max_length=50, null=True)),
                ('description', models.CharField(max_length=1000)),
                ('account_number', models.BigIntegerField()),
                ('accountholder_name', models.CharField(max_length=50)),
                ('ifsc_code', models.CharField(max_length=10)),
                ('funds', models.BigIntegerField(default=0)),
                ('eventname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fundraiser_event', to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventname', models.CharField(max_length=1000, null=True)),
                ('timestamp', models.IntegerField()),
                ('paid', models.BooleanField(default=False)),
                ('amount', models.IntegerField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='donating_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
