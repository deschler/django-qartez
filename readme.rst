django-qartez
==============================================
This app aims to provide better XML sitemaps. At the moment the following XML sitemaps are implemented:

    - qartez.ImagesSitemap: XML images sitemaps according to the specs
      http://www.google.com/support/webmasters/bin/answer.py?answer=178636

    - qartez.StaticSitemap: Sitemap for service pages. Add named patterns or URLs to the sitemap to have it
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
    >>> 'django.contrib.sitemaps',
    >>> 'qartez',
    >>> # ...
    >>> )

Usage and examples
==============================================
We have an imaginary foo app.

Usage example `qartez.ImagesSitemap`
----------------------------------------------
foo/sitemap.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
>>> from django.contrib.sitemaps import Sitemap
>>>
>>> from qartez import ImagesSitemap, StaticSitemap
>>>
>>> from foo.models import FooItem
>>>
>>> # Dictionary to feed to the images sitemap
>>> foo_item_images_info_dict = {
>>>     'queryset': FooItem._default_manager.exclude(image=None), # Base queryset
>>>     'image_location_field': 'image', # Image location
>>>     'image_title_field': 'title', # Image title
>>>     'location_field': 'get_absolute_url' # An absolute URL of the page where image is shown
>>> }
>>>
>>> # Images sitemap
>>> foo_item_images_sitemap = {
>>>     'foo_item_images': ImagesSitemap(foo_item_images_info_dict, priority=0.6),
>>> }
>>>
>>> # Sitemap for service pages like welcome and feedback.
>>> foo_static_sitemap = StaticSitemap(priority=0.1, changefreq='never')
>>> foo_static_sitemap.add_named_pattern('foo.welcome')
>>> foo_static_sitemap.add_named_pattern('foo.contact')
>>>
>>> # Foo items sitemap.
>>> class FooItemSitemap(Sitemap):
>>>     changefreq = "weekly"
>>>     priority = 1.0
>>>
>>>     def location(self, obj):
>>>         return obj.get_absolute_url()
>>>
>>>     def lastmod(self, obj):
>>>         return obj.date_published
>>>
>>>     def items(self):
>>>         return FooItem._default_manager.all()
>>>

foo/models.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
>>> from django.db import models
>>> from django.utils.translation import ugettext_lazy as _
>>> from django.core.urlresolvers import reverse
>>>
>>> FOO_IMAGES_STORAGE_PATH = 'foo-images'
>>>
>>> def _foo_images(instance, filename):
>>>     if instance.pk:
>>>         return '%s/%s-%s' % (FOO_IMAGES_STORAGE_PATH, str(instance.pk), filename.replace(' ', '-'))
>>>     return '%s/%s' % (FOO_IMAGES_STORAGE_PATH, filename.replace(' ', '-'))
>>>
>>> class FooItem(models.Model):
>>>     title = models.CharField(_("Title"), max_length=100)
>>>     slug = models.SlugField(_("Slug"), unique=True)
>>>     body = models.TextField(_("Body"))
>>>     image = models.ImageField(_("Headline image"), blank=True, null=True, upload_to=_foo_images)
>>>     date_published = models.DateTimeField(_("Date published"), blank=True, null=True, \
>>>                                           default=datetime.datetime.now())
>>>     date_created = models.DateTimeField(_("Date created"), blank=True, null=True, auto_now_add=True, editable=False)
>>>     date_updated = models.DateTimeField(_("Date updated"), blank=True, null=True, auto_now=True, editable=False)
>>>
>>>     class Meta:
>>>         verbose_name = _("Foo item")
>>>         verbose_name_plural = _("Foo items")
>>>
>>>     def __unicode__(self):
>>>         return self.title
>>>
>>>     def get_absolute_url(self):
>>>         kwargs = {'slug': self.slug}
>>>         return reverse('foo.detail', kwargs=kwargs)

foo/views.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
>>> from django.shortcuts import render_to_response
>>> from django.template import RequestContext
>>>
>>> from foo.models import FooItem
>>>
>>> def browse(request, template_name='foo/browse.html'):
>>>     queryset = FooItem._default_manager.all().order_by('-date_published')
>>>
>>>     context = {'items': queryset}
>>>
>>>     return render_to_response(template_name, context, context_instance=RequestContext(request))
>>>
>>> def detail(request, slug, template_name='foo/detail.html'):
>>>     try:
>>>         item = FooItem._default_manager.get(slug=slug)
>>>     except Exception, e:
>>>         raise Http404
>>> 
>>>     context = {'item': item}
>>>
>>>     return render_to_response(template_name, context, context_instance=RequestContext(request))
>>>
>>> def welcome(request, template_name='foo/welcome.html'):
>>>     context = {}
>>>     return render_to_response(template_name, context, context_instance=RequestContext(request))
>>>
>>> def contact(request, template_name='foo/contact.html'):
>>>     context = {}
>>>     return render_to_response(template_name, context, context_instance=RequestContext(request))


foo/urls.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
>>> from django.conf.urls import patterns, url
>>>
>>> urlpatterns = patterns('foo.views',
>>>     # Foo items listing URL
>>>     url(r'^$', view='browse', name='foo.browse'),
>>>
>>>     # Contact URL
>>>     url(r'^contact/$', view='contact', name='foo.contact'),
>>>
>>>     # Welcome URL
>>>     url(r'^welcome/$', view='welcome', name='foo.welcome'),
>>>
>>>     # Foo item detail URL
>>>     url(r'^(?P<slug>[\w\-\_\.\,]+)/$', view='detail', name='foo.detail'),
>>> )

qartez.RelAlternateHreflangSitemap
----------------------------------------------
The RelAlternateHreflangSitemap behaves exactly like the django.contrib.sitemaps.Sitemap.

# sitemaps.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
>>> from qartez import RelAlternateHreflangSitemap
>>>
>>> class ArticleSitemap(RelAlternateHreflangSitemap):
>>>     def alternate_hreflangs(self, obj):
>>>         return [('en-us', obj.alternative_object_url),]

License
===================================
GPL 2.0/LGPL 2.1

Support
===================================
For any issues contact me at the e-mail given in the `Author` section.

Author
===================================
Artur Barseghyan <artur.barseghyan@gmail.com>