import requests
import aalib
from celery import task
from PIL import Image as PILImage
from PIL import ImageSequence
from StringIO import StringIO
from .models import Image, ImageFrame
from django.utils.html import escape

ANSI = {
    '7m': ('<i>', '</i>'),  # negative
    '0m': ('', ''),  # default
    '3m': ('<u>', '</u>'),  # italic
    '30;1m': ('<s>', '</s>'),  # gray
}


def process_failure(self, exc, task_id, args, kwargs, einfo):
    image = Image.objects.get(id=args[0])
    image.status = Image.FAILED
    image.save()


# def escape(text):
#     htmlCodes = (
#         ('&', '&amp;'),
#         ('<', '&lt;'),
#         ('>', '&gt;'),
#         ('"', '&quot;'),
#         ("'", '&#39;'),
#     )
#     for char, escaped in htmlCodes:
#         text = text.replace(char, escaped)
#     return text


def _html(ansi):
    html = StringIO()
    last_tag = ('', '')
    for sequence in ansi.split("\x1b["):
        for code, tag in ANSI.items():
            if sequence.startswith(code):
                text = sequence.replace(code, '', 1)
                if text and text != '':
                    text = escape(text)
                    if last_tag[0] != tag[0]:
                        text = '%s%s%s' % (last_tag[1], tag[0], text)
                    html.write(text)
                    last_tag = tag
                break
    html.write(last_tag[1])
    return html.getvalue()


@task(on_failure=process_failure, expires=30)
def process_image(image_id):
    image = Image.objects.get(id=image_id)
    image_response = requests.get(image.url)
    pil_image = PILImage.open(StringIO(image_response.content))

    palette = pil_image.getpalette()
    last_frame = None

    image.duration = pil_image.info.get('duration', 0)
    image.save()

    width = 150
    height = ((pil_image.size[1] * 0.65) * width) / pil_image.size[0]
    screen = aalib.LinuxScreen(width=int(width), height=int(height))

    for counter, frame in enumerate(ImageSequence.Iterator(pil_image)):
        if counter > 100:
            break

        background = PILImage.new("RGBA", frame.size)
        if last_frame:
            frame.putpalette(palette)
            background.paste(last_frame)
        background.paste(frame, mask=pil_image.convert('RGBA'))
        last_frame = background.copy()

        screen.put_image((0, 0), background.convert('L').resize(screen.virtual_size))

        frame, created = ImageFrame.objects.get_or_create(image=image, number=pil_image.tell())
        frame.ansi = screen.render()
        frame.html = _html(frame.ansi)
        frame.save()

    image.status = Image.COMPLETED
    image.save()
