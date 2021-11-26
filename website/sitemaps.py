from django.contrib.sitemaps import Sitemap
from .models import *
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):

    def items(self):
        return ['index', 'ideas', 'categories', 'leaderboard']
    
    def location(self, item):
        return reverse(item)

    