from django.test        import TestCase
from django.test.client import Client
from svc.tests          import TestCaseDep

from org.models  import *
from org.urls    import urlpatterns

class OrgTest (TestCase):

    def setUp (self):

        self.client = Client ()

        ##
        ## TODO: Implement set-up data creation!
        ##

    def tearDown (self):

        pass

    def runTest (self, n = 128):

        ##
        ## $ python -m cProfile manage.py test org.OrgTest.runTest
        ##

        for _ in xrange (n):

            self.test_organisation ()
            self.test_organisation_set ()

            self.test_service ()
            self.test_service_set ()

            self.test_b2c_service ()
            self.test_b2c_service_set ()

            self.test_b2b_service ()
            self.test_b2b_service_set ()

    def test_organisation (self, id = 1):

        rsp = self.client.get ('/org/json/ORGANIZATION/%d/' % id)
        self.failUnlessEqual(rsp.status_code, 200)

    def test_organisation_set (self):

        rsp = self.client.get ('/org/json/ORGANIZATION_SET/')
        self.failUnlessEqual(rsp.status_code, 200)

    def test_service (self, id = 1):

        rsp = self.client.get ('/org/json/SERVICE/%d/' % id)
        self.failUnlessEqual(rsp.status_code, 200)

    def test_service_set (self):

        rsp = self.client.get ('/org/json/SERVICE_SET/')
        self.failUnlessEqual(rsp.status_code, 200)

    def test_b2c_service (self, id = 1):

        rsp = self.client.get ('/org/json/B2C_SERVICE/%d/' % id)
        self.failUnlessEqual(rsp.status_code, 200)

    def test_b2c_service_set (self):

        rsp = self.client.get ('/org/json/B2C_SERVICE_SET/')
        self.failUnlessEqual(rsp.status_code, 200)

    def test_b2b_service (self, id = 1):

        rsp = self.client.get ('/org/json/B2B_SERVICE/%d/' % id)
        self.failUnlessEqual(rsp.status_code, 200)

    def test_b2b_service_set (self):

        rsp = self.client.get ('/org/json/B2B_SERVICE_SET/')
        self.failUnlessEqual(rsp.status_code, 200)
