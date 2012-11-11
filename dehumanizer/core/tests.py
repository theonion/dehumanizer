"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from .models import Image
from .tasks import process_image


class SimpleTest(TestCase):
    def test_simple_process(self):
        image = Image.objects.create(url="http://python.org/favicon.ico")
        process_image(image.id)
        print(image.text)

    def test_facebook_process(self):
        image = Image.objects.create(url="http://sphotos-a.xx.fbcdn.net/hphotos-ash3/179544_10100291371127022_749961118_n.jpg")
        process_image(image.id)
        print(image.text)
