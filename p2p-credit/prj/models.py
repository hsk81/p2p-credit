from django.db     import models
from people.models import *
from org.models    import *

class PROJECT (ACTIVITY):

    team       = models.ManyToManyField (PERSON)
    contact    = models.ForeignKey (PERSON,related_name='%(class)ss_by_contact')
    start_date = models.DateField ()
    end_date   = models.DateField (blank=True, null=True)

    def __unicode__ (self):

        return u'%s: %s to %s with %s' % (self.name, self.start_date,
            self.end_date, self.contact)
