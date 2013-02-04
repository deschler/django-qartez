"""
AUTHOR
    Artur Barseghyan (artur.barseghyan@gmail.com)
"""
import datetime

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse_lazy
from django.utils.functional import lazy

from qartez.constants import REL_ALTERNATE_HREFLANG_SITEMAP_TEMPLATE

class RelAlternateHreflangSitemap(Sitemap):
    """
    Sitemaps: rel="alternate" hreflang="x" implementation. 
    
    Read the specs the specs here http://support.google.com/webmasters/bin/answer.py?hl=en&answer=2620865

    IMPORTANT: When you use this class you have to override the "alternate_hreflangs" method in your sitemap class.
    """
    def __get(self, name, obj, default=None):
        try:
            attr = getattr(self, name)
        except AttributeError:
            return default
        if callable(attr):
            return attr(obj)
        return attr

    def alternate_hreflangs(self, item):
        """
        You should override the "alternate_hreflangs" method in your sitemap class.

        Example:
            from qartez import RelAlternateHreflangSitemap

            class ArticleSitemap(RelAlternateHreflangSitemap):
                def alternate_hreflangs(self, obj):
                    return [('en-us', obj.alternative_object_url),]
        """
        raise NotImplementedError(
            u"""You have to override the "alternate_hreflangs" method in your sitemap class. """
            u"""Refer to "qartez" app documentation for details and examples."""
            )

    def _render_alternate_hreflangs(self, item):
        """
        Renders the tiny bit of XML responsible for rendering the alternate hreflang code.

        @return str
        """
        alternate_hreflangs = self.__get('alternate_hreflangs', item, [])
        output = u""
        if alternate_hreflangs:
            for hreflang in alternate_hreflangs:
                output += REL_ALTERNATE_HREFLANG_SITEMAP_TEMPLATE % {'lang': hreflang[0], 'href': hreflang[1]}
        return output

    def get_urls(self, page=1):
        from django.contrib.sites.models import Site
        current_site = Site.objects.get_current()
        urls = []
        for item in self.paginator.page(page).object_list:
            loc = "http://%s%s" % (current_site.domain, self.__get('location', item))
            url_info = {
                'location': loc,
                'lastmod': self.__get('lastmod', item, None),
                'changefreq': self.__get('changefreq', item, None),
                'priority': self.__get('priority', item, None),
                'alternate_hreflangs': self._render_alternate_hreflangs(item),
            }
            #print self._render_alternate_hreflangs(item)
            urls.append(url_info)
        return urls

class SimpleSitemap(Sitemap):
    """
    Simple sitemap for "service" pages. See constructor docstring for list of accepted (additional) arguments.

    Usage example:
        from qartez import SimpleSitemap
        service_sitemap = SimpleSitemap(priority=0.1, changefreq='never')
        service_sitemap.add_named_pattern('blog.welcome')
        service_sitemap.add_named_pattern('feedback.contact')

        content_types_sitemap = SimpleSitemap(priority=1.0, changefreq='daily')
        content_types_sitemap.add_named_pattern('blog.browse') # Homepage
        content_types_sitemap.add_named_pattern('blog.browse', kwargs={'content_type': 'articles'}) # Articles
        content_types_sitemap.add_named_pattern('blog.browse', kwargs={'content_type': 'downloads'}) # Downloads
    """
    NAMED_PATTERN = 1
    URL = 2

    def __init__(self, *args, **kwargs):
        """
        Constructor. Accepts the following optional keyword-arguments (to be only specified as keyword-arguments).

        @param float priority
        @param str changefreq
        @param datetime.datetime|str lastmod
        """
        if kwargs.has_key('priority'):
            self.priority = kwargs.pop('priority')
        else:
            self.priority = 1.0

        if kwargs.has_key('changefreq'):
            self.changefreq = kwargs.pop('changefreq')
        else:
            self.changefreq = 'never'

        if kwargs.has_key('lastmod'):
            self.lastmod = kwargs.pop('lastmod')
        else:
            self.lastmod = datetime.datetime.now()

        super(SimpleSitemap, self).__init__(*args, **kwargs)
        self._items = []

    def items(self):
        """
        Returns sitemap items.

        @return list
        """
        return self._items

    def location(self, obj):
        return obj['location']

    def add_named_pattern(self, viewname, urlconf=None, args=[], kwargs=None, lastmod=None, changefreq=None, \
                          priority=None):
        """
        Ads a named pattern to the items list.
        """
        try:
            loc = reverse_lazy(viewname, urlconf, args, kwargs)
            self._items.append({
                'location': loc,
                'lastmod': lastmod or self.lastmod,
                'changefreq': changefreq if changefreq else self.changefreq,
                'priority': priority if priority else self.priority
                })
        except Exception, e:
            pass

    def add_url(self, url, lastmod=None, changefreq=None, priority=None):
        """
        Adds a URL to the items list.
        """
        try:
            self.items.append({
                'location': url,
                'lastmod': lastmod or self.lastmod,
                'changefreq': changefreq if changefreq else self.changefreq,
                'priority': priority if priority else self.priority
                })
        except Exception, e:
            pass

    def get_urls(self, *args, **kwargs):
        """
        Make sure nothing breaks if some URL is unresolvable.

        @return list
        """
        try:
            return super(SimpleSitemap, self).get_urls(*args, **kwargs)
        except Exception, e:
            return []
