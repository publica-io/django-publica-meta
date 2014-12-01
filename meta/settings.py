# -*- coding: utf-8 -*-
from django.conf import settings


CONTENT_MODELS = getattr(
    settings, 'METATAGS_CONTENT_MODELS', ('page', )
)
