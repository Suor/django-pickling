from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=127)

    def __str__(self):
        return 'id=%s title=%s' % (self.pk, self.title)
