from base.models import Category
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help='This insert categorical data'
    
    def handle(self, *args, **options):
        Titles=['Bicycle','Bike','Car','Van']

        for Title in Titles:
            Category.objects.create(Title=Title)
            
        self.stdout.write(self.style.SUCCESS("Completed Inserting data"))
       
    




