# Generated by Django 2.1.4 on 2019-01-18 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190118_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='cpf',
            field=models.CharField(max_length=14, verbose_name='CPF'),
        ),
    ]