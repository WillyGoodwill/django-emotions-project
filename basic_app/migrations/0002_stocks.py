# Generated by Django 2.2.12 on 2020-12-09 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='stocks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('AAPL', models.FloatField(blank=True, null=True)),
                ('TSLA', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
