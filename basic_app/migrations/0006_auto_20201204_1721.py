# Generated by Django 2.2.12 on 2020-12-04 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0005_auto_20201130_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='emotions',
            name='currentweather',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='emotions',
            name='emotions',
            field=models.CharField(max_length=100),
        ),
    ]