# Generated by Django 2.1.7 on 2019-02-12 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20190212_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(help_text='Rua tal, 123 - Centro', max_length=255, verbose_name='endereço completo'),
        ),
    ]