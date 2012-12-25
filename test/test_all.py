import unittest, webtest
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

from jwa.models import Picture, Gallery
class AllTest(unittest.TestCase):

    def setUp(self):
        # set up google app engine test db service
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        import main
        self.testapp = webtest.TestApp(main.app)

    def testPicturePrice(self):
        gallery = Gallery(title='g1')
        gallery.put()
        test_price = 1.99
        # price is actualy save in _price_by_cent as int
        # befor saving it convert to 199, then when retrieve it convert back
        picture = Picture(
            gallery=gallery, title='p1', price=test_price
        )
        picture.put()
        # test price is still orignal value
        self.assertEqual(picture.price, test_price)

    def testMainView(self):
        response = self.testapp.get('/')


    def tearDown(self):
        self.testbed.deactivate()


