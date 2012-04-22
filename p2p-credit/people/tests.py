from django.test        import TestCase
from django.test.client import Client
from svc.tests          import TestCaseDep

from people.models      import *

class PeopleTest (TestCase):

    def setUp (self):

        self.client = Client ()

        pl0 = PLACE (zip='CH-8051', city='Zurich'    , state='ZH', country='CH')
        pl0.save ()
        pl1 = PLACE (zip='CH-6900', city='Lugano'    , state='TI', country='CH')
        pl1.save ()
        pl2 = PLACE (zip='CH-9000', city='St. Gallen', state='SG', country='CH')
        pl2.save ()

        c0 = CONTACT (email='hasan.karahan@mail.net')   ; c0.save ()
        c1 = CONTACT (email='tiziano.galli@mail.net')   ; c1.save ()
        c2 = CONTACT (email='vital.schwander@mail.net') ; c2.save ()

        p0 = PERSON (title='Mr.', first='Hasan'  , last='Karahan'  ,
            gender='M', dob='1981-04-30') ; p0.save ()
        p1 = PERSON (title='Mr.', first='Tiziano', last='Galli'    ,
            gender='M', dob='1974-01-01') ; p1.save ()
        p2 = PERSON (title='Mr.', first='Vital'  , last='Schwander',
            gender='M', dob='1982-01-01') ; p2.save ()

        g0 = GROUP (name='Enterpreneurs') ; g0.save ()

        r0 = ROLE (person=p0, group=g0, title='member') ; r0.save ()
        r1 = ROLE (person=p1, group=g0, title='member') ; r1.save ()
        r2 = ROLE (person=p2, group=g0, title='member') ; r2.save ()

    def tearDown (self):

        rs = ROLE.objects.all   () ; rs.delete ()
        gs = GROUP.objects.all  () ; gs.delete ()
        ps = PERSON.objects.all () ; ps.delete ()

    def runTest (self, n = 128):

        ##
        ## $ python -m cProfile manage.py test people.PeopleTest.runTest
        ##

        for _ in xrange (n):

            self.test_place ()
            self.test_place_set ()

            self.test_contact ()
            self.test_contact_set ()

            self.test_person ()
            self.test_person_set ()

            self.test_group ()
            self.test_group_set ()

            self.test_role ()
            self.test_role_set ()

            self.test_activity ()
            self.test_activity_set ()

    def test_place (self, id = 1):

        rsp = self.client.get ('/people/json/PLACE/%d/' % id)
        self.failUnlessEqual(rsp.status_code, 200)

    def test_place_set (self):

        rsp = self.client.get ('/people/json/PLACE_SET/')
        self.failUnlessEqual(rsp.status_code, 200)

    def test_contact (self, id = 1):

        rsp = self.client.get ('/people/json/CONTACT/%d/' % id)
        self.failUnlessEqual(rsp.status_code, 200)

    def test_contact_set (self):

        rsp = self.client.get ('/people/json/CONTACT_SET/')
        self.failUnlessEqual(rsp.status_code, 200)

    def test_person (self, id = 1):

        rsp = self.client.get ('/people/json/PERSON/%d/' % id)
        self.failUnlessEqual(rsp.status_code, 200)

    def test_person_set (self):

        rsp = self.client.get ('/people/json/PERSON_SET/')
        self.failUnlessEqual(rsp.status_code, 200)

    def test_group (self, id = 1):

        rsp = self.client.get ('/people/json/GROUP/%d/' % id)
        self.failUnlessEqual(rsp.status_code, 200)

    def test_group_set (self):

        rsp = self.client.get ('/people/json/GROUP_SET/')
        self.failUnlessEqual(rsp.status_code, 200)

    def test_role (self, id = 1):

        rsp = self.client.get ('/people/json/ROLE/%d/' % id)
        self.failUnlessEqual(rsp.status_code, 200)

    def test_role_set (self):

        rsp = self.client.get ('/people/json/ROLE_SET/')
        self.failUnlessEqual(rsp.status_code, 200)

    def test_activity (self, id = 1):

        rsp = self.client.get ('/people/json/ACTIVITY/%d/' % id)
        self.failUnlessEqual(rsp.status_code, 200)

    def test_activity_set (self):

        rsp = self.client.get ('/people/json/ACTIVITY_SET/')
        self.failUnlessEqual(rsp.status_code, 200)
