from google.appengine.ext import db

class Content(db.Model):
    content = db.TextProperty()

class Gallery(db.Model):
    title = db.StringProperty()
    description = ReferenceProperty(Content)

class Picture(db.Model):
    gallery = db.ReferenceProperty(Gallery)
    title = db.StringProperty()
    # put author here for simplicity, maybe can move to it's own table
    author = db.StringProperty()
    # tag = db.CategoryProperty() add tag table if needed
    width = db.IntegerProperty()
    height = db.IntegerProperty()
    media = db.StringProperty() # or change to dropdown ?
    _price_by_cent = db.IntegerProperty()
    original_available = db.BooleanProperty(default=False)
    description = db.ReferenceProperty(Content)
    create_date = db.DateTimeProperty(auto_now_add=True)
    update_date = db.DateTimeProperty(auto_now=True)

    @property
    def price(self):
        return self._price_by_cent / 100.0

