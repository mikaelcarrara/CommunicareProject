# Generated by Django 2.1.4 on 2019-01-18 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190118_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='cpf',
            field=models.CharField(max_length=14, unique=True, verbose_name='CPF'),
        ),
    ]
