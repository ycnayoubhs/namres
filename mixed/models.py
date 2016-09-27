from __future__ import unicode_literals

from django.db import models

from slugify import slugify

class SMModel(models.Model):
    class Meta:
        abstract = True


class Document(SMModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True)
    context = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Document, self).save(*args, **kwargs) # Call the real save() method
