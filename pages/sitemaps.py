from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def get_protocol(self, protocol=None):
        site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
        if protocol:
            return protocol
        return 'https' if site_url.startswith('https') else 'http'

    def items(self):
        return ['home', 'privacy_policy']

    def priority(self, item):
        return 1.0 if item == 'home' else 0.3

    def location(self, item):
        return reverse(item)
