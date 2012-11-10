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
    text = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)

    def __unicode__(self):
        return self.url

    def message(self):
        if self.status == Image.COMPLETED and self.text:
            return self.text
        elif self.status == Image.PENDING:
            return "IMPROVING REALITY..."
        else:
            return "REALITY IMPROVEMENT FAILED."

    def get_absolute_url(self):
        return "/%s" % self.id
