from django.test        import TestCase
from django.test.client import Client
from svc.tests          import TestCaseDep

from com.models  import *

class ComTest (TestCase):

    def setUp (self):

        self.client = Client ()

        ##
        ## TODO: Implement set-up data creation!
        ##

    def tearDown (self):

        pass

    def runTest (self, n = 128):

        ##
        ## $ python -m cProfile manage.py test com.ComTest.runTest
        ##

        for _ in xrange (n):

            self.test_company ()
            self.test_company_set ()

            self.test_employee ()
            self.test_employee_set ()

    def test_company (self, id = 1):

        rsp = self.client.get ('/com/json/COMPANY/%d/' % id)
        self.failUnlessEqual(rsp.status_code, 200)

    def test_company_set (self):

        rsp = self.client.get ('/com/json/COMPANY_SET/')
        self.failUnlessEqual(rsp.status_code, 200)

    def test_employee (self, id = 1):

        rsp = self.client.get ('/com/json/EMPLOYEE/%d/' % id)
        self.failUnlessEqual(rsp.status_code, 200)

    def test_employee_set (self):

        rsp = self.client.get ('/com/json/EMPLOYEE_SET/')
        self.failUnlessEqual(rsp.status_code, 200)
