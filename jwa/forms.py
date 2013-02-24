from google.appengine.ext import db
from google.appengine.api import images
from jwa import settings
from jwa.models import Gallery, Picture

def watermark(image):
    img = images.Image(images.resize(str(image), 800, 600))
    with open(settings.WATERMARK_PATH, 'rb') as f:
        watermark = images.Image(images.resize(f.read(), img.width, img.height))
        x = (img.width - watermark.width)/2
        y = (img.height- watermark.height)/2 
        return images.composite([
            (img, 0, 0, 1.0, images.TOP_LEFT, ), 
            (watermark, x, y, 0.2, images.TOP_LEFT, ),
        ], img.width, img.height, 0, images.JPEG,)

class Form(object):
    def __init__(self, data={}):
        self.fields = {}
        if isinstance(data, self.model):
            for field in self.field_names:
                if hasattr(data, field):
                    self.fields[field] = getattr(data, field)
            self.instance = data
        else:
            for field in self.field_names:
                value = data.get(field)
                if value != None:
                    self.fields[field] = value
            id = data.get('_id')
            if id:
                self.instance = self.model.get_by_id(int(id))

    def is_valid(self):
        self.errors = {}
        return len(self.errors) == 0

    def save(self):
        cleaned_data = self.cleaned_data
        if not hasattr(self, 'instance'):
            self.instance = self.model(**cleaned_data)
        else:
            for field in cleaned_data:
                setattr(self.instance, field, cleaned_data[field])
        self.instance.put()
        return self.instance

class GalleryForm(Form):
    model = Gallery
    field_names = ['title', 'description'] 

    def is_valid(self):
        is_valid = super(GalleryForm, self).is_valid()
        self.cleaned_data = self.fields.copy()
        title = self.cleaned_data.get('title')
        if not title:
            self.errors['title'] = 'This field is required'

        return len(self.errors) == 0

class PictureForm(Form):
    model = Picture
    field_names = [
        'title', 'author', 'gallery_id', 'image', 'gallery_icon', 
        'media', 'price', 'slider', 'original_available', 
        'description', # 'width', 'height', 
    ] 

    def is_valid(self):
        is_valid = super(PictureForm, self).is_valid()
        self.cleaned_data = self.fields.copy()
        gallery_id = self.cleaned_data.get('gallery_id')
        gallery = Gallery.get_by_id(int(gallery_id))
        if gallery:
            self.cleaned_data['gallery'] = gallery
        else:
            self.errors['gallery'] = 'Can not find the porfolio'
        del self.cleaned_data['gallery_id']

        price = self.cleaned_data.get('price')
        if price:
            try:
                self.cleaned_data['price'] = float(price)
            except ValueError:
                self.errors['price'] = 'Price is not valid'
        else:
            del self.cleaned_data['price']

        self.cleaned_data['original_available'] = bool(
            self.cleaned_data['original_available']
        )

        image = self.cleaned_data.get('image')
        if image == None or len(image) == 0:
            if hasattr(self, 'instance'):
                image = self.instance.image
        if len(image) == 0:
            self.errors['image'] = 'Please upload an image'
        else:
            self.cleaned_data['image'] = db.Blob(watermark(image))
        return len(self.errors) == 0

    def save(self):
        gallery_icon = self.cleaned_data['gallery_icon']
        del self.cleaned_data['gallery_icon']
        self.cleaned_data['slider'] = bool(self.cleaned_data['slider'])
        instance = super(PictureForm, self).save()
        gallery = instance.gallery
        if gallery_icon:
            gallery.icon_picture = instance
            gallery.put()
        else:
            if gallery.icon_picture and gallery.icon_picture.id == instance.id:
                gallery.icon_picture = None
                gallery.put()
        return instance


