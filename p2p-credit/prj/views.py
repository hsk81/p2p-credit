from django.http                 import HttpResponse
from django.http                 import Http404
from django.views.generic.simple import direct_to_template
from django.template             import TemplateDoesNotExist

from people.models  import *
from prj.models     import *

import json

class VIEW:

    def main (request):

	user_id = int (request.REQUEST.get ('user-id', 1))
        user = PERSON.objects.get (id=user_id)

        return direct_to_template (
            request,
            template='prj.html',
            extra_context= {
                'person' : user,
            })

    main = staticmethod (main)

class DATA:

    def info (request):

        js_string = json.dumps ({
            'app' : 'prj',
            'ver' : '0.1'
        })

        return HttpResponse (u'%s\n' % js_string, mimetype='application/json')

    info = staticmethod (info)

    def projects (request):

        try:
            start     = int (request.REQUEST.get('start', '0'))
            limit     = int (request.REQUEST.get('limit', '50'))
            sort      =      request.REQUEST.get('sort', 'name')
            direction =      request.REQUEST.get('dir', 'ASC') # ASC|DESC
            callback  =      request.REQUEST.get('callback', '')

            ps = PROJECT.objects.all ()
            ps = ps.order_by ((direction!='ASC') and ('-'+sort) or (sort))
            pg = ps[start:start+limit]

            records = []
            for prj in pg:

                record = {
                    'id'          : prj.id,
                    'name'        : prj.name,
                    'description' : #TODO!
                        ' '.join (prj.description.split ('<br>'))[:96]
                           .replace ('<b>','').replace ('</b>','')
                           .replace ('<p>','').replace ('</p>','')
                           + '..',
                    'contact'     : str (prj.contact),
                    'start_date'  : str (prj.start_date),
                    'end_date'    : str (prj.end_date),
                }

                records.append (record)

            js_string = (callback and u'%s(%s)' or u'%s%s') % (callback,
                json.dumps ({
                    'totalCount' : ps.count (),
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

    projects = staticmethod (projects)

class POST:

    pass

if __name__ == "__main__":

    pass
