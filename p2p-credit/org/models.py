from django.db     import models
from people.models import *

class ORGANIZATION (GROUP):

    people  = GROUP.members
    address = models.ForeignKey (PLACE, blank=True, null=True)
    contact = models.ForeignKey (CONTACT, blank=True, null=True)

    def __unicode__ (self):

        return u'%s' % self.name

class SERVICE (ACTIVITY):

    provider   = models.ForeignKey (ORGANIZATION)
    start_date = models.DateField ()
    end_date   = models.DateField (blank=True, null=True)

    def __unicode__ (self):

        return u'%s: %s' % (self.provider, self.name)

class B2C_SERVICE (SERVICE):

    class Meta:

        verbose_name = 'B2C Service'

    customer = models.ForeignKey (PERSON)

    def __unicode__ (self):

        return u'%s: %s for %s' % (self.provider, self.name, self.customer)

class B2B_SERVICE (SERVICE):

    class Meta:

        verbose_name = 'B2B Service'

    customer = models.ForeignKey (ORGANIZATION)

    def __unicode__ (self):

        return u'%s: %s for %s' % (self.provider, self.name, self.customer)
