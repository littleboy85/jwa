from jwa import settings, handlers

routes = [
    ('/', handlers.HomeHandler),
    ('/porfolio', handlers.GalleryHandler),
    ('/picture', handlers.PictureHandler),
    ('/picture_edit', handlers.PictureEditHandler),
    ('/gallery_edit', handlers.GalleryEditHandler),
    ('/delete', handlers.DeleteHandler),
    ('/home', handlers.HomeHandler),
    ('/event', handlers.EventHandler),
    ('/contact', handlers.ContactHandler),
    ('/price', handlers.PriceHandler),
    ('/admin', handlers.LoginHandler),
    ('/file', handlers.FileHandler),
]

if settings.DEBUG:
    import gaeunit
    routes += gaeunit.routes

