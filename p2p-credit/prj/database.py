from prj.models    import *
from people.models import *

from datetime import date
from datetime import timedelta

import random

def init (project_no = 5):

    init_prj (project_no)

def init_prj (project_no):

    dts = [timedelta (365*midx) for midx in xrange (1+project_no)]
    dtz = zip (dts[:-1],dts[1:])

    PROJECT.objects.all ().delete ()
    for idx, (dt0, dt1) in enumerate (dtz):

        ps = PERSON.objects.all ()
        ps_size = ps.count ()

        prj = PROJECT.objects.create (
            name        = 'PRJ-%04X' % random.randint (0, 1 << 16),
            description = 'This is a short description: ..',
            contact     = ps [idx % ps_size],
            start_date  = date.today () + dt0,
            end_date    = date.today () + dt1)

        for p in ps: prj.team.add (p)
        print prj
    