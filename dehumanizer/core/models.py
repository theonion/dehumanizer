import datetime
from django.db import models


class Image(models.Model):

    PENDING = 0
    FAILED = 1
    COMPLETED = 2
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (FAILED, 'Failed'),
        (COMPLETED, 'Completed'),
    )

    url = models.URLField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    duration = models.IntegerField(default=0)
    created = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.url

    def get_absolute_url(self):
        return "/image?url=%s" % self.url


class ImageFrame(models.Model):

    image = models.ForeignKey(Image, related_name='frames')
    number = models.IntegerField()
    ansi = models.TextField(null=True, blank=True)
    html = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ("image", "number")
        ordering = ["number"]

    def __unicode__(self):
        return "%s #%s" % (self.image, self.number)
