from jwa.models import Gallery, Picture

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
    field_names = ['title', 'author', 'gallery_id', 'image'] 

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
        
        image = self.cleaned_data.get('image')
        if image == None or len(image) == 0:
            if hasattr(self, 'instance'):
                image = self.instance.image
        if len(image) == 0:
            self.errors['image'] = 'Please upload an image'
        else:
            self.cleaned_data['image'] = image
        return len(self.errors) == 0

  

