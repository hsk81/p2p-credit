from django.test        import TestCase
from django.test.client import Client
from svc.tests          import TestCaseDep

from edu.models  import *

class EduTest (TestCase):

    def setUp (self):

        self.client = Client ()

        ##
        ## TODO: Implement set-up data creation!
        ##

    def tearDown (self):

        pass

    def runTest (self, n = 128):

        ##
        ## $ python -m cProfile manage.py test edu.EduTest.runTest
        ##

        for _ in xrange (n):

            self.test_education ()
            self.test_education_set ()

    def test_education (self, id = 1):

        rsp = self.client.get ('/edu/json/EDUCATION/%d/' % id)
        self.failUnlessEqual(rsp.status_code, 200)

    def test_education_set (self):

        rsp = self.client.get ('/edu/json/EDUCATION_SET/')
        self.failUnlessEqual(rsp.status_code, 200)
