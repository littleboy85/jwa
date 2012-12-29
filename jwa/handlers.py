import cgi, webapp2, jinja2
from google.appengine.api import users
from jwa import forms, settings
from jwa.models import Gallery

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIRS)
)

class BaseHandler(webapp2.RequestHandler):

    def render_to_template(self, template_name, context={}, **kwargs):
        template = jinja_env.get_template(template_name)
        self.response.write(template.render(context))

def login_required(func):
    def _wrapped_view(self, *args, **kwargs):
        user = users.get_current_user()
        if user:
            self.user = user
            func(self, *args, **kwargs)
        else:
            self.redirect(users.create_login_url(self.request.uri))
    return _wrapped_view

class GalleryListHandler(BaseHandler):
    def get(self):
        self.render_to_template('gallery_list.html', {
            'gallery_list': Gallery.all()
        })

class GalleryHandler(BaseHandler):

    @login_required
    def get(self):
        id = self.request.get('_id')
        if id:
            gallery = Gallery.get_by_id(int(id))
            form = forms.GalleryForm(gallery)
        else:
            form = forms.GalleryForm()
        self.render_to_template('gallery.html', {
            'form': form
        })

    @login_required
    def post(self):
        form = forms.GalleryForm(self.request.POST)
        if form.is_valid():
            gallery = form.save()
            #self.redirect('/gallery?_id=%s' % gallery.key().id())
            self.redirect('/')
        else:
            self.render_to_template('gallery.html', {
                'form': form
            })

class HomeHandler(BaseHandler):
    def get(self):
        self.render_to_template('home.html')


class PorfolioHandler(BaseHandler):
    def get(self):
        self.render_to_template('porfolio.html')
class ContactHandler(BaseHandler):
    def get(self):
        self.render_to_template('contact.html')    
        
class EventHandler(BaseHandler):
    def get(self):
        self.render_to_template('event.html')        
class PriceHandler(BaseHandler):
    def get(self):
        self.render_to_template('price.html')        