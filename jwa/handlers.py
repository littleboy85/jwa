import cgi, webapp2, jinja2
from google.appengine.api import users, images
from google.appengine.ext import db
from jwa.models import Gallery, Picture, Content, UploadFile
from jwa.forms import GalleryForm, PictureForm
from jwa import settings

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIRS)
)

def login_required(func):
    def _wrapped_view(self, *args, **kwargs):
        user = users.get_current_user()
        if user:
            self.user = user
            func(self, *args, **kwargs)
        else:
            self.redirect(users.create_login_url(self.request.uri))
    return _wrapped_view

class BaseHandler(webapp2.RequestHandler):

    def render_to_template(self, template_name, context={}, status=200):
        template = jinja_env.get_template(template_name)
        context['admin'] = users.is_current_user_admin()
        context['logout_url'] = users.create_logout_url(self.request.uri)
        self.response.write(template.render(context))
        self.response.set_status(status)

class ContentHandler(BaseHandler):

    def get(self):
        obj = Content.get_by_name(self.content_name, create=True)
        self.render_to_template(self.template, {
            'content': obj,
            'edit': self.request.get('edit')
        })

    @login_required
    def post(self):
        obj = Content.get_by_name(self.content_name, create=True)
        obj.content = self.request.get('content')
        obj.put()
        self.render_to_template(self.template, {
            'content': obj
        })

class HomeHandler(ContentHandler):
    content_name = 'about'
    template = 'home.html'

class ContactHandler(BaseHandler):
    def get(self):
        self.render_to_template('contact.html')    
        
class EventHandler(ContentHandler):
    content_name = 'event'
    template = 'event.html'

class PriceHandler(BaseHandler):
    def get(self):
        self.render_to_template('price.html')        

class LoginHandler(BaseHandler):

    @login_required
    def get(self):
        if users.is_current_user_admin():
            self.redirect('/porfolio')
        else:
            self.redirect(users.create_logout_url(self.request.uri))

class PictureHandler(BaseHandler):
    def get(self):
        id = self.request.get('_id')
        type = self.request.get('type')
        picture = Picture.get_by_id(int(id))
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.write(picture.image)

class GalleryHandler(BaseHandler):

    def get(self):
        id = self.request.get('_id', '1')
        gallery = Gallery.get_by_id(int(id))
        self.render_to_template('porfolio.html', {
            'gallery_list': Gallery.all(),
            'gallery': gallery,
        })

class FormHandler(BaseHandler):
    
    def get_initial(self):
        return {}

    def get_redirect(self, obj):
        return '/'

    def get_context(self, **kwargs):
        return kwargs

    def get(self):
        id = self.request.get('_id')
        if id:
            obj = self.model.get_by_id(int(id))
            form = self.form_cls(obj)
        else:
            form = self.form_cls(self.get_initial())
        self.render_to_template(self.template, self.get_context(form=form))

    @login_required
    def post(self):
        form = self.form_cls(self.request)
        if form.is_valid():
            obj = form.save()
            self.redirect(self.get_redirect(obj))
        else:
            self.render_to_template(self.template, self.get_context(form=form))

class GalleryEditHandler(FormHandler):
    model = Gallery
    form_cls = GalleryForm
    template = 'gallery_form.html'

    def get_redirect(self, obj):
        return '/porfolio?_id=%s' % obj.id

class PictureEditHandler(FormHandler):
    model = Picture
    form_cls = PictureForm
    template = 'picture_form.html'

    def get_initial(self):
        gallery_id = self.request.get('gallery_id')
        if not gallery_id:
            self.abort(404)
        return {'gallery_id': gallery_id}

    def get_redirect(self, obj):
        return '/porfolio?_id=%s&picture_id=%s' % (obj.gallery.id, obj.id)

class FileBrowser(BaseHandler):
    def get(self): 
        self.render_to_template('file_browser.html', {
            'func_num': self.request.get('CKEditorFuncNum'),
            'file_list': UploadFile.all(),
        })

class FileHandler(BaseHandler):
    def get(self):
        pass

    def post(self):
        f = self.request.POST['upload']
        content = str(self.request.get('upload'))
        upload_file = UploadFile(
            blob=db.Blob(content), 
            filename=f.filename,
            type=f.type,
        )
        upload_file.put()
        self.response.write('Upload Success')
        

        
