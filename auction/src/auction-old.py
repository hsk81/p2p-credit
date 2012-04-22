__author__ ="hkarahan"
__date__ ="$Nov 29, 2009 10:47:59 AM$"

#
# price       : maximal,
# share       : maximal, (%, abs)
# share*price : maximal >= share.maximal * price.maximal
#

import sys
from random import randint

def get_bid ():

    sys.stdout.write ("bid [#,$]:")

    try:    amount, price = sys.stdin.readline().split (',')
    except: return None

    amount = int   (amount)
    price  = float (price)

    return amount, price

def get_bids ():

    bids = []
    while True:

        t = get_bid ()
        if t == None:
            break
        bids.append(t)

    return sorted (bids, lambda x,y: int (y[1] - x[1]))

def get_bids_predefined ():

    bids = [(2, 20),
            (3, 15),
            (1, 17),
            (5, 16),
            (2, 16)]

    return sorted (bids, lambda x,y: int (y[1] - x[1]))

def get_bids_random (len = 10):

    bids = map (lambda idx: (randint (1,10), 10 * randint(1,100)), xrange (len))
    return sorted (bids, lambda x,y: int (y[1] - x[1]))

def do_auction (bids):

    not_exec = True
    res_amount = None
    res_price = None
    actual_amount = 0.0
    
    for amount, price in bids:

        actual_amount += amount
        actual_price = total / actual_amount

        print "[#,$; #,$]: (%2d,%.2f); (%2d,%.2f)" % \
            (amount, price, actual_amount, actual_price)

        if actual_price < price and not_exec:
            res_amount = actual_amount
            res_price = actual_price
            not_exec = False
            print "---"

    if res_amount == None or res_price == None:
            res_amount = actual_amount
            res_price = actual_price
            print "!!!"

    return res_amount, res_price

def do_allocation (bids, last_price):

    not_exec = True
    subtotal = 0.0
    for amount, price in bids:

        subtotal += amount * last_price
        if last_price > price and not_exec:

            not_exec = False
            print "---"

        print "[#,$; #,$]: (%2d,%.2f); %.2f; %.2f)" % \
            (amount, last_price, amount * last_price, subtotal)

def do_renormalization (bids, last_price, total):

    subtotal = 0.0
    for amount, price in bids:
        
        if last_price > price: break
        else: subtotal += amount * last_price

    quotient = total / subtotal

    bids = map (lambda (x,y): (quotient * 1000.0*x, y/1000.0), bids)
    do_allocation (bids, last_price/1000.0)

if __name__ == "__main__":

    total = 15000.0
    bids = get_bids_random ()

    print "\n<1: auction>>\n"
    last_amount, last_price = do_auction (bids)
    print "\n<2: allocation>>\n"
    do_allocation (bids, last_price)
    print "\n<3: renormalization>>\n"
    do_renormalization (bids, last_price, total)
