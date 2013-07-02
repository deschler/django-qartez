django-qartez Package
==============================================
This app aims to provide better XML sitemaps. At the moment the following XML sitemaps are implemented:
- qartez.ImagesSitemap: XML images sitemaps according to the specs 
  http://www.google.com/support/webmasters/bin/answer.py?answer=178636
- qartez.SimpleSitemap: Sitemap for service pages. Add named patterns or URLs to the sitemap to have it
  nicely displayed in a separate service XML sitemap.
- qartez.RelAlternateHreflangSitemap: Sitemaps: rel="alternate" hreflang="x" implementation. Read the specs
  the specs here http://support.google.com/webmasters/bin/answer.py?hl=en&answer=2620865

Installation
==============================================
1. Install
----------------------------------------------
Latest stable version on pypi:

    $ pip install django-qartez

Latest stable version from source:

    $ pip install -e hg+http://bitbucket.org/barseghyanartur/qartez@stable#egg=qartez

2. Add 'qartez' to your ``INSTALLED_APPS``
----------------------------------------------
    >>> INSTALLED_APPS = (
    >>> # ...
    >>> 'qartez',
    >>> # ...
    >>> )

3. Copy templates
----------------------------------------------
Copy the file `qartez/templates/qartez/sitemap_rename_and_place_in_global_templates.xml` to your global
templates directory and rename it to just `sitemap.xml`.

Usage and examples
==============================================
We have an imaginary foo app.

Usage example `qartez.ImagesSitemap`
----------------------------------------------
foo/sitemap.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


qartez.RelAlternateHreflangSitemap
----------------------------------------------
The RelAlternateHreflangSitemap behaves exactly like the django.contrib.sitemaps.Sitemap.

# sitemaps.py file example content
from qartez import RelAlternateHreflangSitemap

class ArticleSitemap(RelAlternateHreflangSitemap):
    def alternate_hreflangs(self, obj):
        return [('en-us', obj.alternative_object_url),]
# end sitemaps.py file example content

License
===================================
GPL 2.0/LGPL 2.1

Support
===================================
For any issues contact me at the e-mail given in the `Author` section.

Author
===================================
Artur Barseghyan <artur.barseghyan@gmail.com>