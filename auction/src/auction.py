#! /usr/bin/python

__author__ = "hkarahan"
__date__   = "$Dec 1, 2009 8:39:50 PM$"

import sys
import random

from matplotlib.pyplot import *
from numpy             import *
from optparse          import OptionParser

class BaseBid (object):

    def __init__ (self, min = 0, max = 0, prc = 0):
        
        self.min = min      # minimum desired shares
        self.max = max      # maximum desired shares
        self.prc = prc      # maximum price per share

    def __add__ (self, other):

        _min = self.min + other.min
        _max = self.max + other.max
        _prc = min (self.prc, other.prc)

        return BaseBid(_min, _max, _prc)

    def __str__ (self):

        return "min = %04d, max = %04d, prc = %04d" % \
            (self.min, self.max, self.prc)

class RandomBid (BaseBid):

    def __init__ (self, shares_range = (1, 10), prc_range = (1,100)):

        self.min = 1
        self.max = 0

        while (self.min > self.max):

            self.min = random.randint (shares_range[0], shares_range[1])
            self.max = random.randint (shares_range[0], shares_range[1])

        self.prc = random.randint (prc_range[0], prc_range[1])

    def get_bids (amount = 100, shares_range = (1,10), prc_range = (1,100)):

        bids = map (lambda t: RandomBid(shares_range, prc_range), range(amount))
        bids = sorted (bids, lambda x,y: y.prc - x.prc)

        return bids

    get_bids = staticmethod (get_bids)

class Bid (BaseBid):

    pass

class BidList (object):

    def __init__ (self, bids = []):

        self.bids = bids

    def __str__ (self):

        ss = map (lambda t: t.__str__ (), self.bids)
        return "[" + (', '.join (ss)).strip () + "]"

    def sum (bids):

        return reduce (lambda x,y: x+y, bids, BaseBid(0, 0, bids[0].prc))

    sum = staticmethod (sum)

    def sum_product (bids):

        prc = bids[-1].prc # use minimal prc
        ts = map (lambda t: (t.min * prc, t.max * prc), bids)
        sp = reduce (lambda x,y: (x[0]+y[0], x[1]+y[1]), ts, (0,0))
        
        return sp

    sum_product = staticmethod (sum_product)

class Auction (object):

    def __init__ (self, bid_amount = 100, shares_range = (1, 10), \
                        prc_range = (1,100)):

        self.bids = RandomBid.get_bids (bid_amount, shares_range, prc_range)

    def allocate (self, shares = 5000, amount = 125000):

        sum = Bid (0,0) # sum (min, max)
        pro = Bid (0,0) # sum (min*prc, max*prc)

        for idx, bid in enumerate (self.bids):

            sum.min += bid.min ; pro.min = sum.min * bid.prc
            sum.max += bid.max ; pro.max = sum.max * bid.prc

            if sum.max >= shares: break
            if pro.max >= amount: break
            if sum.min >= shares: break
            if pro.min >= amount: break
            
        return self.bids[:idx+1]

    def plot (self, options):

        from mpl_toolkits.axes_grid.parasite_axes import SubplotHost

        mins = cumsum (array ([bid.min for bid in self.bids]))
        maxs = cumsum (array ([bid.max for bid in self.bids]))

        prcs = array ([bid.prc for bid in self.bids])        
        prcs.sort () ; prcs = prcs[::-1]

        subplot (311)
        title ("Auction Simulations: runs=%s, bids=%s" % \
            (options.runs,options.bids))
        ylabel ("prices * cum. mins & maxs")
        plot (mins * prcs, 'b')
        plot (maxs * prcs, 'r')

        subplot (312)
        ylabel ("cum. mins & maxs")
        plot (mins, 'b')
        plot (maxs, 'r')

        subplot (313)
        xlabel ("bids")
        ylabel ("prices")
        plot (prcs, 'g')

class Simulation (object):

    def do_run (options):

        data = []
        for idx in range(options.runs):

            if options.print_runs:

                print "+%03d:" % idx,

            auction = \
                Auction (bid_amount   = options.bids, \
                         shares_range = (options.shares_min,options.shares_max), \
                         prc_range    = (options.price_min, options.price_max))

            bids = auction.allocate (shares = options.shares, \
                                     amount = options.amount)

            bids_len = len (bids)
            bids_sum = BidList.sum (bids)
            bids_pro = BidList.sum_product (bids)

            if options.print_runs:

                print "bids = %03d," % bids_len,
                print "%s," % bids_sum,
                print "min-sum = %06d, max-sum = %06d" % bids_pro

            if options.plot_runs:

                auction.plot(options)

            data.append ((bids_len, \
                          bids_sum.min, bids_sum.max, bids_sum.prc, \
                          bids_pro[0], bids_pro[1]))

        return array (data)

    do_run = staticmethod (do_run)

    def do_info (options):

        print
        print "+runs             : %s" % options.runs
        print "+bids             : %s" % options.bids
        print "+shares (min,max) : (%s,%s)" % (options.shares_min, options.shares_max)
        print "+price  (min,max) : (%s,%s)" % (options.price_min,  options.price_max)
        print "+shares           : %s" % options.shares
        print "+amount           : %s" % options.amount

    do_info = staticmethod (do_info)

class Statistic (object):

    def get_avg (runs):

        return average (runs, axis = 0)

    get_avg = staticmethod (get_avg)

    def get_std (runs):

        return std (runs, axis = 0)

    get_std = staticmethod (get_std)

    def print_avg (avg):

        print "+avg:",
        print "bids = %03d," % avg[0],
        print "%s," % str (Bid (avg[1], avg[2], avg[3])),
        print "min-sum = %06d, max-sum = %06d" % (avg[4], avg[5])

    print_avg = staticmethod (print_avg)

    def print_std (std):

        print "+std:",
        print "bids = %03d," % std[0],
        print "%s," % str (Bid (std[1], std[2], std[3])),
        print "min-sum = %06d, max-sum = %06d" % (std[4], std[5])

    print_std = staticmethod (print_std)

if __name__ == "__main__":

    parser = OptionParser()

    parser.add_option("-n", "--runs", type="int", dest="runs",       default=100,
                      help="number of simulation to run")
    parser.add_option("-b", "--bids", type="int", dest="bids",       default=1000,
                      help="number of bids per simulation run")
    parser.add_option("--shares_min", type="int", dest="shares_min", default=1,
                      help="minimum shares per bid")
    parser.add_option("--shares_max", type="int", dest="shares_max", default=10,
                      help="maximum shares per bid")
    parser.add_option("--price_min",  type="int", dest="price_min",  default=1,
                      help="minimum prc per share")
    parser.add_option("--price_max",  type="int", dest="price_max",  default=100,
                      help="maximum prc per share")
    parser.add_option("--shares",     type="int", dest="shares",     default=5000,
                      help="maximum number of available shares for emissions")
    parser.add_option("--amount",     type="int", dest="amount",     default=125000,
                      help="minimum amount of money to be raised")

    parser.add_option("-p", "--plot-runs",   action="store_true", dest="plot_runs",
        default=False, help="enables runs' plotting",)
    parser.add_option("-r", "--silent-runs", action="store_false", dest="print_runs",
        default=True,  help="silences runs' output",)
    parser.add_option("-i", "--silent-info", action="store_false", dest="print_info",
        default=True,  help="silences info output")
    parser.add_option("-s", "--silent-stat", action="store_false", dest="print_stat",
        default=True,  help="silences statistics' output")

    if len (sys.argv) == 1:

        (options, args) = parser.parse_args (["--help"])

    else:

        (options, args) = parser.parse_args (sys.argv[1:])

    runs = Simulation.do_run (options)

    if options.print_stat:

        print
        avg = Statistic.get_avg (runs) ; Statistic.print_avg (avg)
        std = Statistic.get_std (runs) ; Statistic.print_std (std)

    if options.print_info:

        Simulation.do_info (options)

    if options.plot_runs:

        subplot (311) ; grid (True)
        subplot (312) ; grid (True)
        subplot (313) ; grid (True)
        show (True)
