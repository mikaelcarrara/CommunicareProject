# Generated by Django 2.1.7 on 2019-03-13 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20190304_1122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registration',
            options={'verbose_name': 'inscrito'},
        ),
        migrations.AddField(
            model_name='registration',
            name='nf',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='NF'),
        ),
        migrations.AddField(
            model_name='registration',
            name='nf_status',
            field=models.CharField(choices=[('', ''), ('P', 'Pendente'), ('E', 'Emitida')], default='P', max_length=1, verbose_name='Situação NF'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Event', verbose_name='evento'),
        ),
    ]
