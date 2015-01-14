# -*- coding: utf-8 -*-
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

    '''

    # Metatag properties values
    author = models.CharField(max_length=155, blank=True)
    description = models.CharField(max_length=155, blank=True)
    keywords = models.CharField(
        max_length=155,
        blank=True,
        help_text='A list of comma separated keywords'
    )

    '''
    OG properties values

    url is og:url
    title is og:title
    image is og:image
    object_type is og:type
    site_name is og:site_name

    '''

    url = models.CharField(max_length=50, blank=True, help_text=(
        'The title of your object as it should appear within the graph, e.g., '
        '"The Rock".'
    ))
    title = models.CharField(max_length=50, blank=True, help_text=(
        'The type of your object, e.g., "video.movie".'
    ))
    image = models.CharField(max_length=50, blank=True, help_text=(
        'An image URL which should represent your object within the graph.'
    ))
    type = models.CharField(max_length=50, blank=True, help_text=(
        'The canonical URL of your object that will be used as its permanent '
        'ID in the graph, e.g., "http://www.imdb.com/title/tt0117500/".'
    ))
    site_name = models.CharField(max_length=50, blank=True, help_text=(
        'If your object is part of a larger web site, the name which should '
        'be displayed for the overall site. e.g., "IMDb".'
    ))

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
        'contenttypes.ContentType',
        limit_choices_to={'model__in': CONTENT_MODELS}
    )
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('content_type', 'object_id')
        verbose_name = 'Metadata Description'

    def __unicode__(self):
        return u'{} :: {}'.format(
            self.content_object.__class__.__name__,
            self.content_object.__unicode__()
        )


class MetatagPath(BaseMetatag):
    path = models.CharField(db_index=True, max_length=255)

    class Meta:
        ordering = ('path', )
        verbose_name = 'Metadata for Path'

    def __unicode__(self):
        return self.path

    def save(self, *args, **kwargs):
        if not self.path.startswith('/'):
            self.path = '/{}'.format(self.path)

        if not self.path.endswith('/'):
            self.path += '/'

        super(MetatagPath, self).save(*args, **kwargs)
