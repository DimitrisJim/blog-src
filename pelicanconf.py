#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Jim Fasarakis-Hilliard'
SITENAME = "Couldn't be buggered"
SITEURL = '' # 'https://dimitrisjim.github.io'
PATH = 'content/'

LOCALE = ('en_GB.utf8', 'en')
TIMEZONE = 'Europe/Athens'
DEFAULT_LANG = 'en'

# Blogroll
LINKS = (('Home','/index.html'),
         ('About','/pages/about-me.html'),
         ('Tags', '/tags.html'),)

SOCIAL = (('Feed','/feeds/all.atom.xml'),
      ('Email','mailto:d.f.hilliard@gmail.com'),
      ('GitHub','https://github.com/DimitrisJim'),
      ('StackOverflow', 'https://stackoverflow.com/users/4952130/jim-fasarakis-hilliard'),
      ('Linkedin', 'https://www.linkedin.com/in/jim-fasarakis-hilliard-b1879487/'),
      ('Instagram', 'https://www.instagram.com/jim.fh/'),
      ('Twitter', 'https://twitter.com/Dimitris__Jim'),)
# Pagination for main page.
DEFAULT_PAGINATION = 4
# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
# Not-Generated:
THEME = 'voce'
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['assets', 'sitemap', 'gravatar']
STATIC_PATHS = ['images']
USER_LOGO_URL = '/images/f1IZs.jpg'

# Visibility on tagline.
TAGS_URL = 'tags.html'
ARCHIVES_URL = 'archives.html'

LOAD_CONTENT_CACHE = False
# Explanatory, applies if :summary: doesn't exist
SUMMARY_MAX_LENGTH = 120
FUZZY_DATES = True
# Pass markdown options, see top level README.md
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {
            'noclasses': True,
            'pygments_style': 'borland',
        },
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
}
# Not using it now but keep it in case.
PYGMENTS_RST_OPTIONS = {
    'linenos': 'table',
    'anchorlinenos': True,
}
# Sitemap
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}
# Google Analytics props.
GOOGLE_ANALYTICS_ID = "UA-99978854-1"
GOOGLE_ANALYTICS_PROP = "Personal Blog"
