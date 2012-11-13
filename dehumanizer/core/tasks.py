import requests
import aalib
from celery import task
from PIL import Image as PILImage
from StringIO import StringIO
from .models import Image

ANSI = {
    '7m': 'i',  # negative
    '0m': 'b',  # default
    '3m': 'u',  # italic
    '30;1m': 's',  # gray
}


def process_failure(self, exc, task_id, args, kwargs, einfo):
    image = Image.objects.get(id=args[0])
    image.status = Image.FAILED
    image.save()


def _html(ansi):
    html = StringIO()
    html.write('<b>')
    last_tag = ANSI['0m']
    for sequence in ansi.split("\x1b["):
        for code, tag in ANSI.items():
            if sequence.startswith(code):
                text = sequence.replace(code, '', 1)
                if text and text != '':
                    text = text.replace(' ', '&nbsp;')
                    text = text.replace('\n', '<br />')
                    text = '</%s><%s>%s' % (last_tag, tag, text)
                    html.write(text)
                    last_tag = tag
                break
    html.write('</%s>' % tag)
    return html.getvalue()


@task(on_failure=process_failure)
def process_image(image_id):
    image = Image.objects.get(id=image_id)
    image_response = requests.get(image.url)
    pil_image = PILImage.open(StringIO(image_response.content))
    width = 150
    height = ((pil_image.size[1] * 0.65) * width) / pil_image.size[0]
    screen = aalib.LinuxScreen(width=int(width), height=int(height))
    screen.put_image((0, 0), pil_image.convert('L').resize(screen.virtual_size))
    image.ansi = screen.render()
    image.save()
    image.html = _html(image.ansi)
    image.status = Image.COMPLETED
    image.save()
