# Generated by Django 3.1.3 on 2020-11-30 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emotions',
            name='emotions',
            field=models.CharField(choices=[('1', 'Страх'), ('2', 'Тоска'), ('3', 'Гнев'), ('4', 'Стыд'), ('5', 'Радость')], default='1', max_length=1),
        ),
    ]