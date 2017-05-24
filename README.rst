Django pickling
===============

Makes django models pickling 2-3 times faster and compact.


Requirements
------------

| Python 2.7 or 3.3+, Django 1.8+


Installation and setup
----------------------

    $ pip install django-pickling

Then add ``django_pickling`` to your ``INSTALLED_APPS``.


CAVEATS
-------

1. No Django version checks are performed.
2. If fields list changes you will see TypeErrors instead of AttributeErrors.

In both cases you should wipe your cache or change keys.
Note that you will need to deal with this anyway,
with django-pickling you'll just get weirder errors.

Another thing is that objects with deferred fields are not optimized.
