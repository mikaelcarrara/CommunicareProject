# Generated by Django 2.1.4 on 2019-01-09 18:46

import communicare.core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='source',
            field=models.ForeignKey(default=communicare.core.models.get_default_source, on_delete=django.db.models.deletion.PROTECT, to='core.Source'),
        ),
    ]