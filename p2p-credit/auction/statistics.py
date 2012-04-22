from django.db.models            import decimal
from django.db.models            import datetime
from django.db.models.aggregates import *
from django.db.models.query      import *

from auction.models              import *

class STATISTICS:

    def basic (auction_id):

        auction = AUCTION.objects.get (id = auction_id)
        bs = BID.objects.filter (auction = auction)
        bs = bs.order_by ('rate')

        ##
        ## TODO: Optimize calculation (by better? using query-sets/numpy)!
        ##

        act_amount = 0
        cum_rate   = decimal.Decimal ('0.00')

        for idx, bid in enumerate (bs):

            act_amount += bid.amount
            cum_rate   += bid.amount * bid.rate

            if act_amount >= auction.target_amount:

                bs = bs[:idx] ; break

        res = {
            'actual_amount' : '%.2f' % act_amount,
            'actual_rate'   : '%.2f' % (cum_rate / (act_amount or 1))
        }

        return res

    basic = staticmethod (basic)

    def extended (auction_id):

        auction = AUCTION.objects.get (id = auction_id)
        bs = BID.objects.filter (auction = auction)
        ss = bs.order_by ('rate')

        ##
        ## TODO: Optimize calculation (by better? using query-sets/numpy)!
        ##

        act_amount = 0
        cum_rate   = decimal.Decimal ('0.00')
        rs         = bs

        for idx, bid in enumerate (ss):

            act_amount += bid.amount
            cum_rate   += bid.amount * bid.rate

            if act_amount >= auction.target_amount:

                rs = bs.order_by ('rate')[:idx] ; break

        sd = auction.start_date
        d0 = datetime.date (sd.year, sd.month, sd.day)
        d1 = datetime.date.today ()

        dates = [d0+datetime.timedelta (i) for i in xrange ((d1-d0).days+1)]

        ##
        ## TODO: Does not work, since days with *no* bids are ignored!
        ##

        ## dt2nob = bs.values ('datestamp').annotate (nob=Count ('id'))

        dt2nob = dict ([(date,0) for date in dates])
        for k2v in bs.values ('datestamp'):

            if dt2nob.has_key (k2v['datestamp']):
                dt2nob [k2v['datestamp']] += 1
            else:
                dt2nob [k2v['datestamp']]  = 1

        d0_nob = min (dt2nob.keys ())
        d1_nob = max (dt2nob.keys ())
        dt2nob = zip (dt2nob.keys (), dt2nob.values ())

        ##
        ## TODO: Does not work, since values.annotate does not deliver
        ##       properly groups (because rs is already ordered and sliced!
        ##

        ## dt2rob = rs.values ('datestamp').annotate (rob=Count ('id'))

        dt2rob = dict ([(date,0) for date in dates])
        for k2v in rs.values ('datestamp'):

            if dt2rob.has_key (k2v['datestamp']):
                dt2rob [k2v['datestamp']] += 1
            else:
                dt2rob [k2v['datestamp']]  = 1

        d0_rob = min (dt2rob.keys ())
        d1_rob = max (dt2rob.keys ())
        dt2rob = zip (dt2rob.keys (), dt2rob.values ())

        res = {
            'nob'        : '%.2f' %
                bs.count (),
            'min_nob'    : '%.2f' %
                min (dt2nob, key=lambda (k,v): v)[1],
            'avg_nob'    : '%.2f' %
                (1.0 * bs.count () / ((d1_nob-d0_nob).days or 1.0)),
            'max_nob'    : '%.2f' %
                max (dt2nob, key=lambda (k,v): v)[1],

            'rob'        : '%.2f' %
                rs.count (),
            'min_rob'    : '%.2f' %
                min (dt2rob, key=lambda (k,v): v)[1],
            'avg_rob'    : '%.2f' %
                (1.0 * rs.count () / ((d1_rob-d0_rob).days or 1.0)),
            'max_rob'    : '%.2f' %
                max (dt2rob, key=lambda (k,v): v)[1],

            'min_rate'   : '%.2f' %
                (rs.aggregate (min=Min('rate'))['min'] or 0.0),
            'avg_rate'   : '%.2f' %
                (cum_rate / (act_amount or 1)),
            'max_rate'   : '%.2f' %
                (rs.aggregate (max=Max('rate'))['max'] or 0.0),

            'sum_amount' : '%.2f' % act_amount,
            'min_amount' : '%.2f' %
                (rs.aggregate (min=Min('amount'))['min'] or 0.0),
            'avg_amount' : '%.2f' %
                (rs.aggregate (avg=Avg('amount'))['avg'] or 0.0),
            'max_amount' : '%.2f' %
                (rs.aggregate (max=Max('amount'))['max'] or 0.0),
        }

        return res

    extended = staticmethod (extended)

if __name__ == "__main__":

    pass
