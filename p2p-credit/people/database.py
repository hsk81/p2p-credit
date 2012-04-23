__author__ = "hsk81"
__date__ = "$Apr 23, 2012 10:15:15 AM$"

################################################################################
################################################################################

from people.models import *

from datetime import date
from datetime import timedelta

import random

################################################################################
################################################################################

def init (person_no = 3):

    init_person (person_no)
    init_place  (person_no)
    init_person_address ()

def init_person (person_no):

    dts = [timedelta (365*midx) for midx in xrange (person_no)]

    PERSON.objects.all ().delete ()
    for idx, dt in enumerate (dts):

        person = PERSON.objects.create (
            title = (idx % 2 == 0) and 'Mr.' or 'Ms.',
            first = 'FN-%04X' % random.randint (0, 1 << 16),
            last = 'LN-%04X' % random.randint (0, 1 << 16),
            gender = (idx % 2 == 0) and 'M' or 'F',
            dob = date.today () + dt,
        )

        print person

def init_place (place_no):
    
    PLACE.objects.all ().delete ()
    for _ in xrange (place_no):

        place = PLACE.objects.create (
            zip = 'ZIP-%04X' % random.randint (0, 1 << 16),
            city = 'CT.%04X' % random.randint (0, 1 << 16),
            state = 'ST.%02X' % random.randint (0, 1 << 8),
            country = 'CY.%04X' % random.randint (0, 1 << 16),
        )

        print place

def init_person_address ():

    for person, place in zip (PERSON.objects.all (), PLACE.objects.all ()):

        person.address = place
        person.address.save ()
        person.save ()

################################################################################
################################################################################
