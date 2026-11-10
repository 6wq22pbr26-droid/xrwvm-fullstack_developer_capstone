import json
from pathlib import Path
from django.conf import settings
from .models import CarMake, CarModel

def initiate():
    data = json.loads((Path(settings.BASE_DIR)/'database/data/car_records.json').read_text())['cars']
    for record in data:
        make, _ = CarMake.objects.get_or_create(name=record['make'])
        CarModel.objects.get_or_create(car_make=make, name=record['model'], year=record['year'], dealer_id=record['dealer_id'], defaults={'type':record['bodyType'], 'mileage':record['mileage']})
