from django.test        import TestCase
from django.test.client import Client
from svc.tests          import TestCaseDep

from auction.models     import *
from people.models      import *
from prj.models         import *

from random             import random
from random             import randint

import people.tests
import prj.tests

class AuctionTest (TestCase):

    def setUp (self, peopleTest=None, prjTest=None):

        self.client = Client ()

        self.peopleTestDep = TestCaseDep (peopleTest, people.tests.PeopleTest)
        self.peopleTestDep.setUp ()

        self.prjTestDep = TestCaseDep (prjTest, prj.tests.PrjTest)
        self.prjTestDep.setUp (self.peopleTestDep)

        AUCTION.objects.create (
            project       = PROJECT.objects.order_by ('?')[0],
            start_date    = '2000-01-01',
            expiry_date   = '2000-04-01',
            target_amount = 1000000,
            target_rate   = '0.08'
        )

    def tearDown (self):

        self.prjTestDep.tearDown ()
        self.peopleTestDep.tearDown ()

    def runTest (self, n = 128):

        ##
        ## $ python -m cProfile manage.py test auction.AuctionTest.runTest
        ##

        for _ in xrange (n):

            self.test_auction ()
            self.test_auction_set ()

            self.test_bid ()
            self.test_bid_set ()

            self.test_post_bid ()

    def test_auction (self, id = 1):

        rsp = self.client.get ('/auction/json/AUCTION/%d/' % id)
        self.failUnlessEqual(rsp.status_code, 200)

    def test_auction_set (self):

        rsp = self.client.get ('/auction/json/AUCTION_SET/')
        self.failUnlessEqual(rsp.status_code, 200)

    def test_bid (self, id = 1):

        rsp = self.client.get ('/auction/json/BID/%d/' % id)
        self.failUnlessEqual(rsp.status_code, 200)

    def test_bid_set (self):

        rsp = self.client.get ('/auction/json/BID_SET/')
        self.failUnlessEqual(rsp.status_code, 200)

    def test_post_bid (self):

        user    = PERSON.objects.order_by ('?')[0]
        auction = AUCTION.objects.order_by ('?')[0]
        amount  = 25 * randint (1,10)
        rate    = random ()

        params = "?user-id=%s&auction-id=%s&amount=%s&rate=%s" % (
             user.id, auction.id, amount, '%2.f' % rate
        )

        rsp = self.client.post ('/auction/post/BID/' + params)
        self.failUnlessEqual(rsp.status_code, 200)
    