"""Utilities for reading configuration from settings."""
from collections import namedtuple
from functools import partial
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.text import slugify

import six
import logging

logger = logging.getLogger(__name__)

# Decorators that can be composed.
PIPES = []
# Placeholder decorators
PIPELINES = []


class Pipe:
    """Configuration class."""

    def __init__(self, function, name, slug, meta, enabled):
        """Initialize Pipe."""
        self.function = function
        self.name = name
        self.slug = slug
        self.meta = meta
        self.enabled = enabled


# Decorators used in codebase.
Pipeline = namedtuple('Pipeline', ['slug', 'name', 'meta'])


def conf_to_pipe(conf):
    """Create Pipe object out of configuration."""
    # if conf is a string type, convert it to
    if isinstance(conf, six.string_types):
        conf = {'function': conf}
    if not isinstance(conf, dict):
        raise ImproperlyConfigured(
            'Dynamicdecorator configuration should be string or dictionay:'
            '%s' % conf)
    # Default enabled value.
    conf['enabled'] = False
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
    if 'meta' not in conf:
        conf['meta'] = {}
    return Pipe(**conf)


def get_pipes():
    """Get pipes from settings."""
    # TODO: If settings does not have PROVIDED_DECORATORS assign it.
    #       we should return default decorators in this case.
    # TODO: PROVIDED_DECORATORS seems to be not used right now.
    if PIPES:
        return PIPES
    for c in settings.DYNAMIC_DECORATORS:
        # Set Default vaues.
        p = conf_to_pipe(c)
        if any(e for e in PIPES
               if p.slug == e.slug):
                raise ImproperlyConfigured(
                    'Duplicate name in decorator configuration: %s' % p)
        PIPES.append(p)
    return PIPES


def get_pipelines():
    """Get pipelines."""
    return PIPELINES


def register_pipeline(slug, name, meta):
    """Register given pipeline."""
    if not isinstance(meta, dict):
        raise ImproperlyConfigured(
            'Meta value of a decorator must be a dictionay:'
            '%s' % meta)
    pipeline = Pipeline(slug, name, meta)
    if not any(p.slug == slug for p in PIPELINES):
        PIPELINES.append(pipeline)
        return pipeline
    else:
        logger.info('[DYNAMIC_DECORATORS] %s is already registered. Ignoring.'
                    % slug)
        return next(p for p in PIPELINES if p.slug == slug)


def get_pipeline_by_slug(slug):
    """Search pipeline by slug value."""
    return next(p for p in PIPELINES if p.slug == slug)


def is_match(pipeline, pipe):
        """Check pipe against pipeline.

        Check if there is any meta property on pipeline that matches with
        pipe.
        """
        # if pipe does not have any meta attribute it automatically matches.
        # if pipe has meta attributes it only matches if all meta attributes
        # that exists on both pipe and pipeline has same values.
        # This relationship is not surjective.
        return not pipe.meta or all(pipe.meta[k] == v
                                    for k, v in pipeline.meta.iteritems()
                                    if k in pipe.meta)


def filter_pipes(pipeline, pipes):
    """Filter given pipes by meta values of current pipeline."""
    return filter(partial(is_match, pipeline), pipes)
