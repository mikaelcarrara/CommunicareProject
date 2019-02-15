# Generated by Django 2.1.5 on 2019-02-11 15:06

import json
from django.db import migrations

from communicare.core.models import FederativeUnit, City


def load_cities(apps, schema_editor):
    with open('contrib/brasil-estados-cidades.json') as data_file:
        data = json.load(data_file)
        cities = []

        for state_object in data['estados']:
            initials = state_object['sigla']
            name = state_object['nome']
            if FederativeUnit.objects.filter(initials=initials).exists():
                federative_unit = FederativeUnit.objects.get(initials=initials)
            else:
                federative_unit = FederativeUnit.objects.create(initials=initials, name=name)
            for city in state_object['cidades']:
                cities.append(City(name=city, uf=federative_unit))

        City.objects.bulk_create(cities)


def unload_cities(apps, schema_editor):
    # Brutally deleting all entries for this model...

    federative_unit_model = apps.get_model("core", "FederativeUnit")
    federative_unit_model.objects.all().delete()

    city_model = apps.get_model("core", "City")
    city_model.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20190211_1303'),
    ]

    operations = [
        migrations.RunPython(load_cities, reverse_code=unload_cities),
    ]