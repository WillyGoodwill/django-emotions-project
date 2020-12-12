# Generated by Django 2.2.12 on 2020-12-10 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0003_auto_20201210_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stocks2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('AAPL', models.FloatField(blank=True, null=True)),
                ('TSLA', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Stocks1',
        ),
    ]