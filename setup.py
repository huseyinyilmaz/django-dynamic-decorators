import logging
import sys

from setuptools import find_packages
from setuptools import setup

logging.basicConfig()

VERSION = '0.1.0'
DESCRIPTION = 'Session level dynamic decorators for django.'


def runtests():
    """Run django tests."""
    import django
    from django.conf import settings
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'dynamicdecorators',
        ),
        MIDDLEWARE=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'dynamicdecorators.middleware.dynamicdecorators_middleware',
        ),
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ],

        ROOT_URLCONF='dynamicdecorators.urls',
        DYNAMIC_DECORATORS=(),
    )
    if hasattr(django, 'setup'):
        # django >= 1.7
        django.setup()
    # This need to be imported after the settings has been configured
    try:
        from django.test.runner import DiscoverRunner
    except ImportError:
        # Django < 1.8
        from django.test.simple import DjangoTestSuiteRunner as DiscoverRunner

    test_runner = DiscoverRunner(verbosity=1, interactive=False)
    failures = test_runner.run_tests([])
    sys.exit(failures)


setup(
    name='django-dynamic-decorators',
    version=VERSION,
    description=DESCRIPTION,
    url='https://github.com/huseyinyilmaz/django-dynamic-decorators',
    author='Huseyin Yilmaz',
    author_email='yilmazhuseyin@gmail.com',
    packages=find_packages(),
    py_modules=['dynamicdecorators'],
    include_package_data=True,
    zip_safe=False,
    test_suite='setup.runtests',
    tests_require=[
        'Django>=1.8.0',
        'six',
    ]
)
