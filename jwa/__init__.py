import cgi, webapp2, jinja2
from jwa import settings, handlers

routes = [
    ('/', handlers.HomeHandler),
    ('/gallery', handlers.GalleryHandler),
    ('/home',handlers.HomeHandler),
    ('/showporfolio',handlers.ShowPorfolioHandler),
    ('/porfolio',handlers.PorfolioHandler),
    ('/event',handlers.EventHandler),
    ('/contact',handlers.ContactHandler),
    ('/price',handlers.PriceHandler),
]

if settings.DEBUG:
    import gaeunit
    routes += gaeunit.routes

