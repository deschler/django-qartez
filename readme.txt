AUTHOR
    Artur Barseghyan (artur.barseghyan@gmail.com)

DESCRIPTION
    This app aims to provide better XML sitemaps. At the moment the following XML sitemaps are implemented:
        * qartez.RelAlternateHreflangSitemap: Sitemaps: rel="alternate" hreflang="x" implementation. Read the specs
          the specs here http://support.google.com/webmasters/bin/answer.py?hl=en&answer=2620865
        * qartez.SimpleSitemap: Sitemap for services pages. Add named patterns or URLs to the sitemap to have it
          nicely displayed in a separate service XML sitemap.

INSTALLATION
    * Install the qartez with pip:
          pip install -e hg+http://bitbucket.org/barseghyanartur/qartez#egg=qartez
    * Add 'qartez' to your ``INSTALLED_APPS`` in the global settings.py.
    * Copy the file "qartez/templates/qartez/sitemap_rename_and_place_in_global_templates.xml" to your global
      templates directory and rename it to just "sitemap.xml".

USAGE AND EXAMPLES
    The RelAlternateHreflangSitemap behaves exactly like the django.contrib.sitemaps.Sitemap.

    # sitemaps.py file example content
    from qartez import RelAlternateHreflangSitemap

    class ArticleSitemap(RelAlternateHreflangSitemap):
        def alternate_hreflangs(self, obj):
            return [('en-us', obj.alternative_object_url),]
    # end sitemaps.py file example content

REQUIREMENTS

TODOS
