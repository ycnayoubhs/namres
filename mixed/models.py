from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify

class SMModel(models.Model):
    class Meta:
        abstract = True


class Document(SMModel):
    CONVERTERS = (
        ('N', 'Normal'),
        ('S', 'Server List'),
    )

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True)
    context = models.TextField()
    converter = models.CharField(max_length=1, choices=CONVERTERS, default='N', null=True, blank=True)
    is_deleted = models.BooleanField(db_column='isDeleted', default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Document, self).save(*args, **kwargs) # Call the real save() method
