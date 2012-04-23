__author__ = "hsk81"
__date__ = "$Apr 23, 2012 10:15:15 AM$"

################################################################################
################################################################################

from people.models  import *
from prj.models import *
from auction.models import *

from datetime import date
from datetime import timedelta

import random

################################################################################
################################################################################

def init (auction_no = 7, bid_no = 11):

    init_auction (auction_no)
    init_bid (bid_no)

def init_auction (auction_no):

    dts = [timedelta (30*midx) for midx in xrange (1 + auction_no)]
    dtz = zip (dts[:-1],dts[1:])
    
    AUCTION.objects.all ().delete ()
    for prj in PROJECT.objects.all ():
        for idx, (dt0,dt1) in enumerate (dtz):

            auction = AUCTION.objects.create (
                project = prj,
                start_date  = prj.start_date + dt0,
                expiry_date = prj.start_date + dt1,
                target_amount = "%s" % random.randint (2250,2750),
                target_rate = "%.2f" % (8.00 + 0.25 * idx))

            print auction

def init_bid (bid_no):

    BID.objects.all ().delete ()
    for prs in PERSON.objects.all ():
        for auction in AUCTION.objects.all ():
            for _ in xrange (bid_no):

                bid = BID.objects.create (
                    auction = auction,
                    lender = prs,
                    amount = random.randint (20,30),
                    rate = "%.2f" % (7.50 + random.random ()))

                print bid

################################################################################
################################################################################
