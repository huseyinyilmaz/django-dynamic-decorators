django-dynamic-decorators
=========================

Django app that enables decorators to be applied to views on the fly.

(Work in progress)

Description
===========

This will be an application that enables views to be decorated with list of decorators. There will be a web interface for this application. Through this interface, users will be able to choose decorators from a list and those decorators will be applied only for that specific user. That way, they will not be effecting other people.

This will be usefull for development and testing. There can be decorators that changes some settings values, disable/enable applciations like django-pipeline. So developers will be able to see errors in uncompressed format.

Using python-placebo, It will be possible to mock api interfaces for current user.

Planned Features
================

* Web interface that allow users to see users.
* If disabled, it will not have any performance penalty.
* There should be a generic permission system, so people should be able to enable it only certain group of people.
* There should be a list of default decorators provided. Like, `Disable cache` decorator.
* Configuration should be able do done in 3 different ways. Those 3 options will provide
  configuration to be done in different stages of initialization. Default way will be to
  provide {str: str} type dictionary in settings.
* Decorators should be activated for whole project with a middleware or it should be activated by marking views one by one.
* In the ui, there should be list of decorators to choose from also if multiple views are marked there should be list of views to choose from. user should be able to choose view -> decorator list.
