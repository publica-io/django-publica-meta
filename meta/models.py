# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.forms.models import model_to_dict

from .settings import CONTENT_MODELS


###
# MODELS
###
class BaseMetatag(models.Model):
    '''
    This class represent the whole meta tags class.

    url is og:url
    title is og:title
    image is og:image
    object_type is og:type
    site_name is og:site_name

    '''

    # Meta properties values
    author = models.CharField(max_length=155, blank=True)
    description = models.CharField(max_length=155, blank=True)
    keywords = models.CharField(
        max_length=155,
        blank=True,
        help_text='A list of comma separated keywords'
    )

    # OG properties values
    url = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=50, blank=True)
    image = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=50, blank=True)
    site_name = models.CharField(max_length=50, blank=True)

    class Meta:
        abstract = True

    def build_tags(self):
        obj_dict = model_to_dict(self)

        def _values(names):
            return [{
                'name': name,
                'value': value
            } for name, value in obj_dict.items() if name in names and
                value.strip() != ''
            ]

        return {
            'metatags': _values(['author', 'description', 'keywords']),
            'ogtags': _values(['url', 'title', 'image', 'type', 'site_name'])
        }


class MetatagModelInstance(BaseMetatag):
    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to={'model__in': CONTENT_MODELS}
    )
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('content_type', 'object_id')
        verbose_name = 'Metadata for Model'


class MetatagPath(BaseMetatag):
    path = models.CharField(db_index=True, max_length=255)

    def __unicode__(self):
        return self.path

    class Meta:
        ordering = ('path', )
        verbose_name = 'Metadata for Path'
