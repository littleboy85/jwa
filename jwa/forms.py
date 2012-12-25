from jwa.models import Gallery

class GalleryForm(object):

    def __init__(self, data={}):
        fields = ['title', 'description']
        self.fields = {}
        if isinstance(data, Gallery):
            for field in fields:
                if hasattr(data, field):
                    self.fields[field] = getattr(data, field)
            self.instance = data
        else:
            for field in fields:
                if data.has_key(field):
                    self.fields[field] = data[field]

    def is_valid(self):
        self.errors = {}
        cleaned_data = self.fields
        title = cleaned_data.get('title') or ''
        if not title:
            self.errors['title'] = 'This field is required'

        self.cleaned_data = cleaned_data
        return len(self.errors) == 0

    def save(self):
        cleaned_data = self.cleaned_data
        gallery = Gallery(**cleaned_data)
        gallery.put()
        return gallery

   

