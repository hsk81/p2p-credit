from django.db     import models
from people.models import *
from org.models    import *

class EDUCATION (B2C_SERVICE):

    ##
    ## TODO: Admin interface lacks proper renaming! E.g. it does not show for
    ##       institute the label 'institute' but 'provider'; and it does not
    ##       show for graduate the label 'graduate' but 'customer'.
    ##

    class Meta:

        verbose_name_plural = 'education'

    institute       = B2C_SERVICE.provider
    graduate        = B2C_SERVICE.customer
    degree          = models.CharField (max_length=256, blank=True, null=True)
    field           = models.CharField (max_length=256, blank=True, null=True)
    graduation_date = models.DateField (blank=True, null=True)

    def __unicode__(self):

        if self.degree and self.field:
            return u'%s: %s in %s, %s' % \
                (self.graduate, self.degree, self.field, self.institute)
        elif self.degree:
            return u'%s: %s, %s' % (self.graduate, self.degree, self.institutee)
        elif self.field:
            return u'%s: %s, %s' % (self.graduate, self.field, self.institute)
        else:
            return u'%s: %s' % (self.graduate, self.institute)
