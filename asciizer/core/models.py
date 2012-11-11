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
    ansi = models.TextField(null=True, blank=True)
    html = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)

    def __unicode__(self):
        return self.url

    def get_absolute_url(self):
        return "/image?url=%s" % self.url
