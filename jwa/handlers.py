import cgi, webapp2, jinja2, zipfile, StringIO, json, poster, urllib
from google.appengine.api import users, images, urlfetch
from google.appengine.ext import db, blobstore
from google.appengine.ext.webapp import blobstore_handlers
from jwa import settings
from jwa.models import Gallery, Picture, Content
from jwa.forms import GalleryForm, PictureForm, watermark

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

    def get_context(self, **kwargs):
        obj = Content.get_by_name(self.content_name, create=True)
        return {
            'content': obj,
            'edit': self.request.get('edit'),
        }

    def get(self):
        context = self.get_context()
        self.render_to_template(self.template, context)

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

    def get_context(self, **kwargs):
        context = super(HomeHandler, self).get_context(**kwargs)
        qs = Picture.all().filter('slider =', True)
        context['slider_pictures'] = [picture for picture in qs]
        return context

class ContactHandler(ContentHandler):
    content_name = 'contact'
    template = 'contact.html'
        
class EventHandler(ContentHandler):
    content_name = 'event'
    template = 'event.html'

class PriceHandler(ContentHandler):
    content_name = 'price-and-ordering'
    template = 'price.html'

class LoginHandler(BaseHandler):

    @login_required
    def get(self):
        if users.is_current_user_admin():
            self.redirect('/porfolio')
        else:
            self.redirect(users.create_logout_url(self.request.uri))

class GalleryHandler(BaseHandler):

    def get(self):
        id = self.request.get('_id')
        picture_id = self.request.get('picture_id')
        picture = Picture.get_by_id(int(picture_id)) if picture_id else None
        gallery_list = Gallery.all().order('-create_date')

        if id:
            gallery = Gallery.get_by_id(int(id))
        else:
            if picture is None:
                gallery = gallery_list.get()
            else:
                gallery = picture.gallery
        if gallery and (picture is None or picture.gallery.id != gallery.id):
            picture = gallery.pictures.get()

        self.render_to_template('porfolio.html', {
            'gallery_list': gallery_list,
            'gallery': gallery,
            'cur_picture': picture,
        })

class PictureHandler(BaseHandler):

    def get(self):
        id = self.request.get('_id')
        width = self.request.get('width')
        height = self.request.get('height')
        picture = Picture.get_by_id(int(id))
        image = images.Image(picture.image)
        width = int(width) if width else image.width
        height = int(height) if height else image.height
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.write(images.resize(picture.image, width, height))

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

    def is_valid(self, form):
        obj = form.save()
        self.redirect(self.get_redirect(obj))

    @login_required
    def post(self):
        form = self.form_cls(self.request)
        if form.is_valid():
            self.is_valid(form)
        else:
            self.render_to_template(self.template, self.get_context(form=form))

class GalleryEditHandler(FormHandler):
    model = Gallery
    form_cls = GalleryForm
    template = 'gallery_form.html'

    def is_valid(self, form):
        obj = form.save()
        image_zip = self.request.get('image_zip')
        try:
            myzip = zipfile.ZipFile(StringIO.StringIO(image_zip), 'r')
            for name in myzip.namelist():
                image = myzip.read(name)
                picture = Picture(gallery=obj, image=db.Blob(watermark(image)))
                picture.put()
        except zipfile.BadZipfile:
            pass
        self.redirect(self.get_redirect(obj))

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

class DeleteHandler(BaseHandler):

    def get(self):
        obj = db.get(self.request.get('key'))
        self.render_to_template('delete.html', {
            'obj': obj,
            'obj_url': self.request.get('obj_url', self.request.referer),
            'success_url': self.request.get('success_url'),
        })

    def post(self):
        obj = db.get(self.request.get('key'))
        obj.delete()
        self.redirect(self.request.get('success_url'))

poster.streaminghttp.register_openers()
class CKUploadHandler(BaseHandler):
    def post(self):
        f = self.request.POST['upload']
        value = self.request.get('upload')
        param = poster.encode.MultipartParam(
            'file', filename=f.filename, filetype=f.type, fileobj=f.file,
        )
        data, headers = poster.encode.multipart_encode([param])
        self.response = urlfetch.fetch(
            url=blobstore.create_upload_url('/upload'),
            payload=''.join(data), method=urlfetch.POST, headers=headers,
        )

class CKBrowseHandler(BaseHandler):
    def get(self):
        func_num = self.request.get('CKEditorFuncNum')
        self.render_to_template('file_browser.html', {
            'func_num': func_num,
            'blob_infos': blobstore.BlobInfo.all(),
        })

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        if resource:
            resource = str(urllib.unquote(resource))
            blob_info = blobstore.BlobInfo.get(resource)
            self.send_blob(blob_info)
        else:
            self.response.write(json.dumps({
                'blob_info': [
                    {'key': str(blob_info.key())}
                    for blob_info in blobstore.BlobInfo.all()
                ]
            }))

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        self.response.write(json.dumps({
            'key': str(self.get_uploads('file')[0].key())
        }))

        
