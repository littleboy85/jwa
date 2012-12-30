import cgi, webapp2, jinja2
from jwa import settings, handlers

routes = [
    ('/', handlers.HomeHandler),
    ('/porfolio', handlers.GalleryHandler),
    ('/picture', handlers.PictureHandler),
    ('/picture_edit', handlers.PictureEditHandler),
    ('/gallery_edit', handlers.GalleryEditHandler),
    ('/home',handlers.HomeHandler),
    ('/event',handlers.EventHandler),
    ('/contact',handlers.ContactHandler),
    ('/price',handlers.PriceHandler),
]

if settings.DEBUG:
    import gaeunit
    routes += gaeunit.routes

