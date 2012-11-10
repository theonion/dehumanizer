import requests
import aalib
from celery import task
from PIL import Image as PILImage
from StringIO import StringIO
from asciizer.core.models import Image


@task
def process_image(image_id):
    image = Image.objects.get(id=image_id)
    image_response = requests.get(image.url)
    pil_image = PILImage.open(StringIO(image_response.content))
    screen = aalib.LinuxScreen(width=int(pil_image.size[0] * 2 / 5), height=pil_image.size[1] / 5)
    screen.put_image((0, 0), pil_image.convert('L').resize(screen.virtual_size))
    image.text = screen.render()
    image.status = Image.COMPLETED
    image.save()
