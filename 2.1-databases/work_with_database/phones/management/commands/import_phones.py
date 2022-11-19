import csv

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            # TODO: Добавьте сохранение модели
            db_value = Phone(id=int(phone['id']),
                             name=phone['name'],
                             image=phone['image'],
                             price=float(phone['price']),
                             release_date=phone['release_date'],
                             lte_exists=bool(phone['lte_exists'], ),
                             slug=phone['name'].replace(" ", "-").lower()
                             )
            db_value.save()
        print("Из файла phones.csv все импортировано в ДБ.")
