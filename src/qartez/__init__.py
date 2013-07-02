__title__ = 'qartez'
__version__ = '0.3'
__build__ = 0x000003
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('ImagesSitemap', 'StaticSitemap', 'RelAlternateHreflangSitemap',)

import datetime

from django.contrib.sitemaps import Sitemap, GenericSitemap
from django.core.urlresolvers import reverse_lazy
from django.utils.functional import lazy
from django.contrib.sites.models import Site

from qartez.constants import REL_ALTERNATE_HREFLANG_SITEMAP_TEMPLATE
from qartez.settings import PREPEND_LOC_URL_WITH_SITE_URL, PREPEND_IMAGE_LOC_URL_WITH_SITE_URL


class ImagesSitemap(GenericSitemap):
    """
    Class for image sitemap. Implemented accordings to specs specifed by Google
    http://www.google.com/support/webmasters/bin/answer.py?answer=178636
    """
    def __init__(self, info_dict, priority=None, changefreq=None):
        """
        Constructor.

        :param dict info_dict:
        :param priority float:
        :param str changefreq:
        """
        self.image_location_field = info_dict.get('image_location_field', None)
        self.image_caption_field = info_dict.get('image_caption_field', None)
        self.image_title_field = info_dict.get('image_title_field', None)
        if self.image_title_field:
            self.image_title_field = unicode(self.image_title_field)
        self.image_geo_location_field = info_dict.get('image_geo_location_field', None)
        self.image_license_field = info_dict.get('image_license_field', None)
        self.location_field = info_dict.get('location_field', None)
        super(ImagesSitemap, self).__init__(info_dict, priority, changefreq)

    def image_location(self, item):
        """
        Gets our image location.
        """
        if self.image_location_field is not None:
            return getattr(item, self.image_location_field)
        return None

    def image_caption(self, item):
        """
        Gets our image caption.
        """
        if self.image_caption_field is not None:
            return getattr(item, self.image_caption_field)
        return None

    def image_title(self, item):
        """
        Gets our image title.
        """
        if self.image_title_field is not None:
            return getattr(item, self.image_title_field)
        return None

    def image_geo_location(self, item):
        """
        Gets our image geo location.
        """
        if self.image_geo_location_field is not None:
            return getattr(item, self.image_geo_location_field)
        return None

    def image_license(self, item):
        """
        Gets our image geo location.
        """
        if self.image_license_field is not None:
            return getattr(item, self.image_license_field)
        return None

    def location(self, obj):
        if self.location_field is not None:
            try:
                location_field = getattr(obj, self.location_field)
                if callable(location_field):
                    return location_field()
                else:
                    return location_field
            except Exception, e:
                return None
        return obj.get_absolute_url()

    def __get(self, name, obj, default=None):
        try:
            attr = getattr(self, name)
        except AttributeError:
            return default
        if callable(attr):
            return attr(obj)
        return attr

    def get_urls(self, page=1):
        current_site = Site.objects.get_current()
        urls = []
        for item in self.paginator.page(page).object_list:
            loc = self.__get('location', item, None)
            if loc and PREPEND_LOC_URL_WITH_SITE_URL:
                loc = "http://%s%s" % (unicode(current_site.domain), unicode(loc))

            image_loc = self.__get('image_location', item, None)
            if image_loc and PREPEND_IMAGE_LOC_URL_WITH_SITE_URL:
                try:
                    image_loc = "http://%s%s" % (unicode(current_site.domain), unicode(image_loc))
                except Exception, e:
                    continue

            url_info = {
                'location': loc,
                'image_location': image_loc,
                'image_caption': self.__get('image_caption', item, None),
                'image_title': self.__get('image_title', item, None),
                'image_license': self.__get('image_license', item, None),
                'image_geo_location': self.__get('image_geo_location', item, None),
                'lastmod': self.__get('lastmod', item, None),
                'changefreq': self.__get('changefreq', item, None),
                'priority': self.__get('priority', item, None)
            }
            urls.append(url_info)
        return urls


class StaticSitemap(Sitemap):
    """
    Sitemap for ``static`` pages. See constructor docstring for list of accepted (additional) arguments.

    :example:
    >>> from qartez import StaticSitemap
    >>> service_sitemap = StaticSitemap(priority=0.1, changefreq='never')
    >>> service_sitemap.add_named_pattern('blog.welcome')
    >>> service_sitemap.add_named_pattern('feedback.contact')
    >>>
    >>> content_types_sitemap = StaticSitemap(priority=1.0, changefreq='daily')
    >>> content_types_sitemap.add_named_pattern('blog.browse') # Homepage
    >>> content_types_sitemap.add_named_pattern('blog.browse', kwargs={'content_type': 'articles'}) # Articles
    >>> content_types_sitemap.add_named_pattern('blog.browse', kwargs={'content_type': 'downloads'}) # Downloads
    """
    NAMED_PATTERN = 1
    URL = 2

    def __init__(self, *args, **kwargs):
        """
        Constructor. Accepts the following optional keyword-arguments (to be only specified as keyword-arguments).

        :param float priority:
        :param str changefreq:
        :param datetime.datetime|str lastmod:
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

        super(StaticSitemap, self).__init__(*args, **kwargs)
        self._items = []

    def items(self):
        """
        Returns sitemap items.

        :return list:
        """
        return self._items

    def location(self, obj):
        return obj['location']

    def add_named_pattern(self, viewname, urlconf=None, args=[], kwargs=None, lastmod=None, changefreq=None, \
                          priority=None):
        """
        Ads a named pattern to the items list.

        :param str viewname:
        :param urlconf:
        :param list args:
        :param dict kwargs:
        :param lastmod:
        :param str changefreq:
        :param float priority:
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

        :param str url:
        :param lastmod:
        :param str changefreq:
        :param float priority:
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

        :return list:
        """
        try:
            return super(StaticSitemap, self).get_urls(*args, **kwargs)
        except Exception, e:
            return []


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

        :return str:
        """
        alternate_hreflangs = self.__get('alternate_hreflangs', item, [])
        output = u""
        if alternate_hreflangs:
            for hreflang in alternate_hreflangs:
                output += REL_ALTERNATE_HREFLANG_SITEMAP_TEMPLATE % {'lang': hreflang[0], 'href': hreflang[1]}
        return output

    def get_urls(self, page=1):
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
