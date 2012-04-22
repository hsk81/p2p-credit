from django.db     import models
from people.models import *
from org.models    import *

class COMPANY (ORGANIZATION):

    class Meta:

        verbose_name_plural = 'companies'

    INC_CHOICES = (

        ##
        ## US specific business entity forms
        ##

        ('GP'   , 'General Partnership' ),
        ('LP'   , 'Limited Partnership' ),
        ('LLP'  , 'Limited Liability Partnership' ),
        ('LLC'  , 'Limited Liability Company' ),
        ('Inc.' , 'Incorporation' ),
        ('Corp.', 'Corporation' ),

        ##
        ## Swiss specific business entity forms
        ##

        ('AG'   , u'Aktiengesellschaft' ),
        ('GmbH' , u'Gesellschaft mit beschraenkter Haftung' ),

    )

    inc = models.CharField (max_length=16, choices=INC_CHOICES,
                            verbose_name='incorporation')

    trade_register    = models.CharField (max_length=256, blank=True, null=True)
    ticker            = models.CharField (max_length=256, blank=True, null=True)
    registration_date = models.DateField (blank=True, null=True)
    security_register = None ## TODO
    auditing          = None ## TODO

    def __unicode__ (self):

        return u'%s %s' % (self.name, self.inc)

class EMPLOYEE (ROLE):

    ##
    ## TODO: Admin interface lacks polymorphism! E.g. self.group instead of
    ##       self.company is shown on the add-employee form.
    ##

    def __init__ (self, *args, **kwargs):

        super (EMPLOYEE, self).__init__ (*args, **kwargs)
        if self.id:
            
            self.company = self.group.organization.company

    profession = models.CharField (max_length=256)
    start_date = models.DateField ()
    end_date   = models.DateField (blank=True, null=True)

    def __unicode__ (self):

        return u'%s: %s @ %s' % (self.person, self.title, \
            self.group.organization.company)
