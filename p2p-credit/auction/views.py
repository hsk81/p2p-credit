from django.http                 import HttpResponse
from django.http                 import Http404
from django.views.generic.simple import direct_to_template
from django.template             import TemplateDoesNotExist
from django.core                 import serializers
from django.core.cache           import cache
from django.db                   import connection

from people.models  import *
from edu.models     import *
from com.models     import *
from auction.models import *

from statistics     import *

import datetime
import hashlib
import numpy
import json

class VIEW:

    def main (request, id):

        auction = AUCTION.objects.get (id=id)
        user_id = int (request.REQUEST.get ('user-id', 1))
        user = PERSON.objects.get (id=user_id)

        educations = EDUCATION.objects.all () \
            .filter (customer = auction.project.contact)

        education = (educations.count () > 0) \
            and educations[0] \
            or  None

        employees = EMPLOYEE.objects.all () \
            .filter (person = auction.project.contact) \
            .order_by ('end_date')

        employee = (employees.count () > 0) \
            and employee[0] \
            or  None

        return direct_to_template (
            request,
            template='auction.html',
            extra_context= {
                'auction'   : auction,
                'project'   : (auction) and auction.project or None,
                'person'    : user,
                'education' : education,
                'employee'  : employee,
            })

    main = staticmethod (main)

class DATA:

    def info (request):
        
        js_string = json.dumps ({
            'app' : 'auction',
            'ver' : '0.1'
        })

        return HttpResponse (u'%s\n' % js_string, mimetype='application/json')

    info = staticmethod (info)

    def bids_order (sort, dir):

        if   sort == 'rate'   : order = ['rate', 'amount'] ## TODO: in model?
        elif sort == 'amount' : order = ['amount', 'rate'] ## TODO: in model?

        elif sort in ['first', 'last']:

            order = ['lender__%s' % sort, 'rate', 'amount']

        elif sort in ['city', 'state', 'zip', 'country']:

            order = ['lender__address__%s' % sort, 'rate', 'amount']

        if dir != 'ASC':

            order[0] = '-' + order[0]

        return order

    bids_order = staticmethod (bids_order)

    def bid_status (cum_amount, target_amount, prev_status):

        if (cum_amount > target_amount): res = 'cross'
        else:                            res = 'tick'

        if prev_status == 'tick' and res == 'cross':

            res = 'tick-last'
        
        return res

    bid_status = staticmethod (bid_status)

    def bids (request):

        try:
            user_id    = int (request.REQUEST.get('user-id', 0))
            auction_id = int (request.REQUEST.get('auction-id', 0))
            auction    = AUCTION.objects.get (id= auction_id)
            
            start      = int (request.REQUEST.get('start', '0'))
            limit      = int (request.REQUEST.get('limit', '50'))
            sort       =      request.REQUEST.get('sort', 'rate')
            direction  =      request.REQUEST.get('dir', 'ASC') # ASC|DESC
            callback   =      request.REQUEST.get('callback', '')

            uid = hashlib.sha256 (json.dumps ({
                'user-id'    : user_id,
                'auction-id' : auction_id,
                'page-size'  : limit,
                'page-index' : start / limit,
                'page-sort'  : sort,
                'page-dir'   : direction
            })).hexdigest ()

            if cache.has_key (uid):

                bs = BID.objects.filter (auction = auction_id)
                pg = cache.get (uid) ## @SEE: cache_page
                cache.delete (uid)

            else:

                bs = BID.objects.filter (auction = auction_id)
                bs = bs.order_by (*DATA.bids_order (sort, direction))
                pg = bs[start:start+limit]

            cursor = connection.cursor ()
            query = cursor.execute ( \
                "SELECT a.id, SUM (a.amount) AS cum_amount FROM \
                    (SELECT * FROM auction_bid WHERE auction_id=%s ORDER BY rate) a, \
                    (SELECT * FROM auction_bid WHERE auction_id=%s ORDER BY rate) b  \
                 WHERE a.rowid <= b.rowid GROUP BY b.rowid, b.rate", \
                 [auction_id, auction_id] \
            )

            id2cum = dict (query.fetchall ()) ##TODO: Slow?! Improve ..

            prev_status = None
            records = []
            for bid in pg:

                record = {
                    'id'         : bid.id,
                    'first'      : bid.lender.first,
                    'last'       : bid.lender.last,
                    'amount'     : bid.amount,
                    'rate'       : str (bid.rate),
                    'cum_amount' : id2cum [bid.id],
                    'status'     : DATA.bid_status (id2cum [bid.id],
                                       auction.target_amount, prev_status)
                }

                if bid.lender.address :

                 ## if bid.lender.address.line1 and bid.lender.address.line1:
                 ##     record['street'] = u'%s %s' % \
                 ##         (bid.lender.address.line1,bid.lender.address.line2)
                 ## else:
                 ##     record['street'] = bid.lender.address.line1

                    record['city']    = bid.lender.address.city
                    record['state']   = bid.lender.address.state
                    record['zip']     = bid.lender.address.zip
                    record['country'] = bid.lender.address.country

                records.append (record) ; prev_status = record['status']

            js_string = (callback and u'%s(%s)' or u'%s%s') % (callback,
                json.dumps ({
                    'totalCount' : bs.count (),
                    'records'    : records,
                    'success'    : True
                })
            )
            
        except Exception as ex:

            js_string = (callback and u'%s(%s)' or u'%s%s') % (callback,
                json.dumps ({
                    'totalCount' : 0,
                    'records'    : [],
                    'success'    : False,
                    'exception'  : ex.__repr__ ()
                })
            )

        return HttpResponse(u'%s\n' % js_string, mimetype='application/json')

    bids = staticmethod (bids)

    def statistics_basic (request):

        try:
            auction_id = int (request.REQUEST.get('auction-id', 0))

            sb = STATISTICS.basic (auction_id)
            sb['success'] = True
            js_string = json.dumps (sb)

        except Exception as ex:

            js_string = json.dumps ({
                'actual_amount' : '?',
                'actual_rate'   : '?',
                'success'       : False,
                'exception'     : ex.__repr__ ()
            })

        return HttpResponse (u'%s\n' % js_string, mimetype='application/json')

    statistics_basic = staticmethod (statistics_basic)

    def statistics_extended (request):

        try:
            auction_id = int (request.REQUEST.get('auction-id', 0))

            se = STATISTICS.extended (auction_id)
            se['success'] = True
            js_string = json.dumps (se)

        except Exception:

            js_string = json.dumps ({
                'nob'        : '?',
                'min_nob'    : '?',
                'avg_nob'    : '?',
                'max_nob'    : '?',

                'rob'        : '?',
                'min_rob'    : '?',
                'avg_rob'    : '?',
                'max_rob'    : '?',

                'min_rate'   : '?',
                'avg_rate'   : '?',
                'max_rate'   : '?',

                'min_amount' : '?',
                'avg_amount' : '?',
                'max_amount' : '?',

                'success'    : False
            })

        return HttpResponse (u'%s\n' % js_string, mimetype='application/json')

    statistics_extended = staticmethod (statistics_extended)

    def auctions_by_project (request):

        try:
            project_id = int (request.REQUEST.get('project-id', '0'))

            start      = int (request.REQUEST.get('start', '0'))
            limit      = int (request.REQUEST.get('limit', '50'))
            sort       =      request.REQUEST.get('sort', 'start_date')
            direction  =      request.REQUEST.get('dir', 'ASC') # ASC|DESC
            callback   =      request.REQUEST.get('callback', '')

            os = AUCTION.objects.filter (project = project_id)
            os = os.order_by ((direction!='ASC') and ('-'+sort) or (sort))
            pg = os[start:start+limit]

            records = []
            for act in pg:

                sb = STATISTICS.basic (act.id)

                record = {
                    'id'            : act.id,
                    'is_active'     : act.expiry_date >= datetime.date.today (),
                    'start_date'    : str (act.start_date),
                    'expiry_date'   : str (act.expiry_date),
                    'target_amount' : int (act.target_amount),
                    'target_rate'   : float (act.target_rate),
                    'actual_amount' : sb ['actual_amount'],
                    'actual_rate'   : sb ['actual_rate'],
                }

                records.append (record)

            js_string = (callback and u'%s(%s)' or u'%s%s') % (callback,
                json.dumps ({
                    'totalCount' : os.count (),
                    'records'    : records,
                    'success'    : True
                })
            )

        except Exception as ex:

            js_string = (callback and u'%s(%s)' or u'%s%s') % (callback,
                json.dumps ({
                    'totalCount' : 0,
                    'records'    : [],
                    'success'    : False,
                    'exception'  : ex.__repr__ ()
                })
            )

        return HttpResponse (u'%s\n' % js_string, mimetype='application/json')

    auctions_by_project = staticmethod (auctions_by_project)

class POST:

    def cache_page (request, id):

     ## import time ; time.sleep (5.00)

        try:
            user_id    = int (request.REQUEST.get('user-id', 0))
            auction_id = int (request.REQUEST.get('auction-id', 0))
            page_size  = int (request.REQUEST.get('page-size', '50'))
            sort       =      request.REQUEST.get('sort', 'rate')
            dir        =      request.REQUEST.get('dir', 'ASC') # ASC|DESC

            bs = BID.objects.filter (auction = auction_id)
            bs = bs.order_by (*DATA.bids_order (sort,dir))

            bs_list = list (bs); bs_size = len (bs_list)
            obj2idx = dict (zip (bs_list, xrange (bs_size)))
            bid_idx = obj2idx [BID.objects.get (id=id)]

            page_idx = bid_idx / page_size
            page_row = bid_idx % page_size

            uid = hashlib.sha256 (json.dumps ({
                'user-id'    : user_id,
                'auction-id' : auction_id,
                'page-size'  : page_size,
                'page-index' : bid_idx / page_size,
                'page-sort'  : sort,
                'page-dir'   : dir
            })).hexdigest ()

            cache.set (uid, bs_list[page_idx*page_size:(page_idx+1)*page_size])

            page_info = {
                'size'   : page_size,
                'index'  : page_idx,
                'row'    : page_row,
            }

            js_string = json.dumps ({
                'total_count' : bs_size,
                'page_info'   : page_info,
                'success'     : True
            })

        except Exception as ex:

            js_string = json.dumps ({
                'total_count' : 0,
                'page_info'   : {},
                'success'     : False,
                'exception'   : ex.__repr__ ()
            })

        return HttpResponse(u'%s\n' % js_string, mimetype='application/json')

    cache_page = staticmethod (cache_page)

    def bid (request):

        try:    user_id  = int (request.REQUEST.get('user-id', 0))
        except: user_id = None

        try:    auction_id = int (request.REQUEST.get('auction-id', 0))
        except: auction_id = None

        try:    amount = int (request.REQUEST.get('amount', 0))
        except: amount = None

        try:    rate = float (request.REQUEST.get('rate', 0.0))
        except: rate = None

        try:    user = PERSON.objects.get (id=user_id)
        except: user = None

        try:    auction = AUCTION.objects.get (id=auction_id)
        except: auction = None

        is_valid = (user != None) \
            and (auction != None) \
            and (amount != None and amount > 0) \
            and (rate != None and rate > 0.0)
               
        if is_valid:

            if  auction.expiry_date < datetime.date.today ():

                js_string = json.dumps({
                    'success' : False,
                    'resinfo' : 'AUCTION_EXPIRED'
                })

            else:

                bid = BID (
                    auction = auction,
                    lender  = user,
                    amount  = amount,
                    rate    = '%.2f' % rate
                )

                try:
                    bid.save()

                    js_string = json.dumps({
                        'success' : True,
                        'resinfo' : 'BID_SUBMITTED',
                        'id'      : bid.id
                    })

                except Exception as ex:

                    js_string = json.dumps({
                        'success'   : 'False',
                        'resinfo'   : 'DB_WRITE_FAILED',
                        'exception' : ex.__repr__ ()
                    })
        else:

            errors = {}

            if user == None:
                errors['user-id']    = 'invalid value'
            if auction == None:
                errors['auction-id'] = 'invalid value'
            if amount == None or amount <= 0:
                errors['amount']     = 'invalid value'
            if rate == None or rate <= 0.0:
                errors['rate']       = 'invalid value'

            js_string = json.dumps ({
                'success'   : False,
                'resinfo'   : 'INVALID_INPUT',
                'errors'    : errors
            })

        return HttpResponse (u'%s\n' % js_string, mimetype='application/json')

    bid = staticmethod (bid)

if __name__ == "__main__":

    pass
