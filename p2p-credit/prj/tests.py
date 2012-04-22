from django.test        import TestCase
from django.test.client import Client
from svc.tests          import TestCaseDep

from prj.models         import *
from people.models      import *

import people.tests

class PrjTest (TestCase):

    def setUp (self, peopleTest = None):

        self.client = Client ()

        self.peopleTestDep = TestCaseDep (peopleTest, people.tests.PeopleTest)
        self.peopleTestDep.setUp ()

        prj = PROJECT.objects.create (
            name       = 'P2P Banking',
            contact    = PERSON.objects.order_by ('?')[0],
          # team       = PERSON.objects.all (),
            start_date = '2000-01-01'
        )

        for p in PERSON.objects.all ():

            prj.team.add (p)

    def tearDown (self):

        self.peopleTestDep.tearDown ()

    def runTest (self, n = 128):

        ##
        ## $ python -m cProfile manage.py test prj.PrjTest.runTest
        ##

        for _ in xrange (n):

            self.test_project ()
            self.test_project_set ()

    def test_project (self, id = 1):

        rsp = self.client.get ('/project/json/PROJECT/%d/' % id)
        self.failUnlessEqual(rsp.status_code, 200)

    def test_project_set (self):

        rsp = self.client.get ('/project/json/PROJECT_SET/')
        self.failUnlessEqual(rsp.status_code, 200)
