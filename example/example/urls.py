from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from foo.sitemap import foo_item_images_sitemap, foo_static_sitemap, FooItemSitemap

sitemaps = {
    'foo-items': FooItemSitemap,
    'foo-static': foo_static_sitemap
}

admin.autodiscover()

urlpatterns = patterns('',
    # Foo URLs
    (r'^foo/', include('foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Sitemaps
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    (r'^sitemap-foo-images\.xml$', 'qartez.views.render_images_sitemap', {'sitemaps': foo_item_images_sitemap}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)
