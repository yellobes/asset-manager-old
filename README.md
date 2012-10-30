About dj-trunk
==============

A collection of apps that I have written, bundled into one project.

I have tried to make an effort to make all of the apps portable, but the
fact is, they aren't. You are going to have to modify the settings.py at a minimum
to get any of these apps to work.
Many of them depend on external libraries.
The code is poorly written.
The views are not class based.

Anyway, most of these apps attempt to adhere to REST fairly strictly.
Some of them, or parts of some of them might be useful to someone.


This django project utilizes these fine 3rd party modules:

django-haystack     :: github.com/toastdriven/django-haystack
whoosh search       :: bitbucket.org/mchaput/whoosh
modular settings    :: github.com/brack3t/django-modular-settings
django-registration :: bitbucket.org/ubernostrum/django-registration


***

Assets
------

Assets is an application to manage your company's assets! Light and simple, it's built around search functionality provided by the haystack api. Supports, images, supporting documents, and much, much more!

