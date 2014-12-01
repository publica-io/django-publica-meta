# -*- coding: utf-8 -*-
from django import template
from django.core.exceptions import ImproperlyConfigured

from ..models import MetatagModelInstance, MetatagPath


register = template.Library()


@register.inclusion_tag('meta/meta.html', takes_context=True)
def get_metadata(context):
    try:
        path = context['request'].path
        path = path if path.startswith('/') else '/{}'.format(path)

    except KeyError:
        raise ImproperlyConfigured(
            'Please add "django.core.context_processors.request" to your '
            'TEMPLATE_CONTEXT_PROCESSORS setting.'
        )

    try:
        meta = MetatagPath.objects.get(path=path)
        return meta.build_tags()
    except MetatagPath.DoesNotExist:
        return {
            'metatags': [],
            'ogtags': []
        }

    # TODO Handle the reverse GFK relationship lookup (slug field I guess)
