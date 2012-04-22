from django.db     import models
from people.models import *
from prj.models    import *

class AUCTION (models.Model):

    def __init__ (self, *args, **kwargs):

        super (AUCTION, self).__init__ (*args, **kwargs)
        if self.id:

            self.borrower = self.project.contact

    project       = models.ForeignKey (PROJECT)
    start_date    = models.DateField ()
    expiry_date   = models.DateField ()
    target_amount = models.PositiveIntegerField ()
    target_rate   = models.DecimalField (max_digits=5, decimal_places=2)

    def statistics_basic (self, id):

        auction = AUCTION.objects.get (id = id)
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

    def statistics_extended (self):

        ##
        ## TODO: bs, dt2nob & rs, dt2rob
        ##

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

    def __unicode__ (self):

        return u'%s: %s to %s, %s @ %.2f%%' % (self.project, self.start_date,
            self.expiry_date, self.target_amount, float (self.target_rate))
    
class BID (models.Model):

    auction   = models.ForeignKey (AUCTION)
    lender    = models.ForeignKey (PERSON)
    amount    = models.PositiveIntegerField ()
    rate      = models.DecimalField (max_digits=5, decimal_places=2)

    datestamp = models.DateField (auto_now_add=True)
    timestamp = models.DateTimeField (auto_now_add=True)

    def __unicode__ (self):

        return u'%s - %06d @ %05.2f for %s from %s' % (self.timestamp, \
            int (self.amount), float (self.rate), self.auction.project.name, \
            self.lender)
    