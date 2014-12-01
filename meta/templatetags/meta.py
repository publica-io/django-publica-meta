# -*- coding: utf-8 -*-
from django import template
from django.core.exceptions import ImproperlyConfigured

from ..models import MetatagModelInstance, MetatagPath


register = template.Library()


@register.inclusion_tag('meta/meta.html', takes_context=True)
def get_metadata(context, obj=None):
    meta = None

    try:
        meta = MetatagModelInstance.objects.get(
            content_type__model=obj.__class__.__name__.lower(),
            object_id=obj.pk
        )
    except (AttributeError, MetatagModelInstance.DoesNotExist):
        # We did not pass any Object therefore there is not available metadata
        # or here is no metadata for the current object
        pass

    try:
        meta = MetatagPath.objects.get(path=context['request'].path)
    except KeyError:
        raise ImproperlyConfigured(
            'Please add "django.core.context_processors.request" to your '
            'TEMPLATE_CONTEXT_PROCESSORS setting.'
        )
    except MetatagPath.DoesNotExist:
        # There is no metadata set for the current path
        pass

    try:
        return meta.build_tags()
    except AttributeError:
        # There is not any metadata for the current object nor path, return
        # empty lists instead
        return {
            'metatags': [],
            'ogtags': []
        }
