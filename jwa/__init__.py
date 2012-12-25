import cgi, webapp2, jinja2
from jwa import settings, handlers

routes = [
    ('/', handlers.GalleryListHandler),
    ('/gallery', handlers.GalleryHandler),
]

if settings.DEBUG:
    import gaeunit
    routes += gaeunit.routes

