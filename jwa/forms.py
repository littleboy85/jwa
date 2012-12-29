from jwa.models import Gallery, Picture

class Form(object):
    def __init__(self, data={}):
        self.fields = {}
        if isinstance(data, Gallery):
            for field in self.field_names:
                if hasattr(data, field):
                    self.fields[field] = getattr(data, field)
            self.instance = data
        else:
            for field in self.field_names:
                if data.has_key(field):
                    self.fields[field] = data[field]

    def is_valid(self):
        self.errors = {}
        self.cleaned_data = self.fields.copy()
        return len(self.errors) == 0

    def save(self):
        cleaned_data = self.cleaned_data
        obj = self.model(**cleaned_data)
        obj.put()
        return obj

class GalleryForm(Form):
    model = Gallery
    field_names = ['title', 'description'] 

    def is_valid(self):
        is_valid = super(GalleryForm, self).is_valid()
        title = self.cleaned_data.get('title')
        if not title:
            self.errors['title'] = 'This field is required'
        return len(self.errors) == 0

class PictureForm(Form):
    model = Picture
    field_names = ['title', 'author', 'gallery'] 

    def is_valid(self):
        is_valid = super(PictureForm, self).is_valid()
        gallery_id = self.cleaned_data.get('gallery')
        gallery = Gallery.get_by_id(int(gallery_id))
        if gallery:
            self.cleaned_data['gallery'] = gallery
        else:
            self.errors['gallery'] = 'Can not find the porfolio'
        return len(self.errors) == 0

  

