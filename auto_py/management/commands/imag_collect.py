from django.core.management.base import BaseCommand, CommandError
from api.models import Image

class Command(BaseCommand):

  def handle(self, *args, **options):
      del_images=Image.objects.all().filter(ref=1)

      for image in del_images:
          image.delete()
          print(image.name)
