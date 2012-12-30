from google.appengine.ext import db
from google.appengine.api import images

class BaseModel(object):
    @property
    def id(self):
        return self.key().id()

class Gallery(db.Model, BaseModel):
    title = db.StringProperty(required=True)
    description = db.TextProperty()

class Picture(db.Model, BaseModel):
    gallery = db.ReferenceProperty(
        Gallery, required=True, collection_name='pictures'
    )
    image = db.BlobProperty()
    title = db.StringProperty(required=True)
    # put author here for simplicity, maybe can move to it's own table
    author = db.StringProperty()
    # tag = db.CategoryProperty() add tag table if needed
    width = db.IntegerProperty()
    height = db.IntegerProperty()
    media = db.StringProperty() # or change to dropdown ?
    _price_by_cent = db.IntegerProperty()
    original_available = db.BooleanProperty(default=False)
    description = db.TextProperty()
    create_date = db.DateTimeProperty(auto_now_add=True)
    update_date = db.DateTimeProperty(auto_now=True)

    def __init__(self, price=None, image=None, *args, **kwargs):
        if price != None:
            kwargs['_price_by_cent'] = int(price * 100)
        if image != None:
            image = db.Blob(str(image))
        super(Picture, self).__init__(*args, image=image, **kwargs)

    @property
    def price(self):
        if self._price_by_cent == None:
            return None
        return self._price_by_cent / 100.0

    @price.setter
    def price(self, value):
        self._price_by_cent = value * 100

