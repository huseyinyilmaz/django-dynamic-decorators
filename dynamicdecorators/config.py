"""
Utilities for reading configuration from settings.
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.text import slugify

import six


class Decorator:
    """Provided decorator to add to pipeline."""

    PROVIDED_DECORATORS = []

    def __init__(self, name, function, meta=None):
        self.name = name
        self.fuction = function
        self.meta = meta if meta is not None else {}

    @staticmethod
    def normalize_configuration(conf):
        if isinstance(conf, six.string_types):
            conf = {'function': conf}

        if not isinstance(conf, dict):
            raise ImproperlyConfigured(
                'Dynamicdecorator configuration should be string or dictionay:'
                '%s' % conf)
        # Only mandatory field is function:
        if 'function' not in conf:
            raise ImproperlyConfigured(
                'Configuration do not have function item: %s' % conf)
        # If name is not defined use function name as name
        if 'name' not in conf:
            conf['name'] = conf['function']
        if 'slug' not in conf:
            conf['slug'] = conf['name']
        # Ensure that slug is slugified
        conf['slug'] = slugify(conf['slug'])
        # Group will be used in interface
        if 'group' not in conf:
            conf['group'] = ''
        return conf

    @classmethod
    def register(cls, *args, **kwargs):
        decorator = cls(*args, **kwargs)

        return decorator

    # TODO add memoize
    @classmethod
    def get_provided_decorators(cls):
        # TODO: In settings we should be able to provide only path
        #       and system should be able to create dict structure.
        # TODO: If settings does not have PROVIDED_DECORATORS assign it.
        #       we should return
        provided_decorators = []
        for d in settings.DYNAMIC_DECORATORS:
            # Set Default vaues.
            d = cls.normalize_configuration(d)
            if any(e for e in cls.PROVIDED_DECORATORS
                   if d['slug'] == e['slug']):
                    raise ImproperlyConfigured(
                        'Duplicate name in decorator configuration: %s' % d)
            provided_decorators.append(d)
        return provided_decorators


class Pipeline:
    """Added pipeline to create decorators."""

    # list of registered decorators.
    PIPELINES = set()

    def __init__(self, slug, meta):
        self.slug = slug
        self.meta = meta

    @classmethod
    def by_slug(cls, slug):
        return next(p for p in cls.PIPELINES if p.slug == slug)

    @classmethod
    def register(cls, slug, meta):
        """Register a decorator.

        We want to keep a list of decorators applied because each one of them will
        have its own configuration and interface.

        Also registration should be idempotent. Because sometimes middlewares gets,
        initialized multiple times. In that case we want to use only one.
        """
        pipeline = cls(slug, meta)
        if not any(p.slug == slug for p in cls.PIPELINES):
            cls.PIPELINES.add(pipeline)
            return pipeline
        else:
            return None


    @classmethod
    def get_registered_decorators(cls):
        """Return all registered decorators"""
        return cls.PIPELINES
