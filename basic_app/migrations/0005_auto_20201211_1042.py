# Generated by Django 2.2.12 on 2020-12-11 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0004_auto_20201210_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks2',
            name='date',
            field=models.DateField(),
        ),
    ]
