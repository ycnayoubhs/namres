from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class SMModel(models.Model):
    class Meta:
        abstract = True


class CustomConverter(SMModel):
    OUTPUT_TYPE = (
        ('F', 'Function'),
        ('S', 'String'),
    )

    name = models.CharField(max_length=20, unique=True)
    context = models.TextField()
    output = models.CharField(max_length=20, unique=True)
    output_type = models.CharField(max_length=1, choices=OUTPUT_TYPE, default='F')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Document(SMModel):
    CONVERTERS = (
        ('N', 'Normal'),
        ('S', 'Server List'),
    )

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True)
    context = models.TextField()
    converter = models.CharField(max_length=1, choices=CONVERTERS, default='N', null=True, blank=True)
    custom_converter = models.ForeignKey(CustomConverter, null=True, blank=True)
    is_deleted = models.BooleanField(db_column='isDeleted', default=False)

    user = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Document, self).save(*args, **kwargs) # Call the real save() method
