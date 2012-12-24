import unittest, webtest
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

class FooTestCase(unittest.TestCase):

    def setUp(self):
        # set up google app engine test db service
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        import main
        self.testapp = webtest.TestApp(main.app)

    def testHello(self):
        response = self.testapp.get('/')
        print response

    def tearDown(self):
        self.testbed.deactivate()

if __name__ == '__main__':
    unittest.main()
