import unittest, webtest
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

class TestModel(db.Model):
    pass

class FooTestCase(unittest.TestCase):

    def setUp(self):
        # set up google app engine test db service
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        self.testapp = webtest.TestApp(webapp2.WSGIApplication([('/', )]))

    def tearDown(self):
        self.testbed.deactivate()

if __name__ == '__main__':
    unittest.main()
