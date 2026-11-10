import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djangoapp.populate import initiate
class Command(BaseCommand):
    help='Idempotently import the provided course car records.'
    def handle(self,*args,**options):
        initiate()
        username=os.getenv('DJANGO_SUPERUSER_USERNAME');password=os.getenv('DJANGO_SUPERUSER_PASSWORD')
        if username and password and not get_user_model().objects.filter(username=username).exists():
            get_user_model().objects.create_superuser(username,'',password)
        self.stdout.write('Course car records imported.')
