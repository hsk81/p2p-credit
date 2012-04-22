from django.db import models

class PLACE (models.Model):

    ##
    ## TODO: If line1 is false but line2 not, it's a validation error!
    ##

    line1   = models.CharField (max_length=256, blank=True, null=True)
    line2   = models.CharField (max_length=256, blank=True, null=True)
    zip     = models.CharField (max_length=256)
    city    = models.CharField (max_length=256)
    state   = models.CharField (max_length=256)
    country = models.CharField (max_length=256)

    def __unicode__ (self):

        if self.line1 and self.line2:
            return u'%s %s, %s %s' % \
                (self.line1, self.line2, self.zip, self.city)
        elif self.line1:
            return u'%s, %s %s' % \
                (self.line1, self.zip, self.city)
        else:
            return u'%s %s' % (self.zip, self.city)

class CONTACT (models.Model):

    phone   = models.CharField (max_length=256, blank=True, null=True)
    mobile  = models.CharField (max_length=256, blank=True, null=True)
    email   = models.EmailField (max_length=256, unique=True)
    website = models.URLField (max_length=256, blank=True, null=True)

    def __unicode__ (self):

        return u'%s' % self.email

class PERSON (models.Model):

    class Meta:

        verbose_name_plural = 'people'

    TITLE_CHOICES = (
        ('Mr.' , 'Mister' ),
        ('Ms.' , 'Miss'   ),
        ('Dr.' , 'Doctor' )
    )

    GENDER_CHOICES = (
        ('M', 'Male'   ),
        ('F', 'Female' ),
    )

    title  = models.CharField (max_length=3, choices=TITLE_CHOICES)
    first  = models.CharField ('first name', max_length=256)
    last   = models.CharField ('last name', max_length=256)
    gender = models.CharField (max_length=1, choices=GENDER_CHOICES)
    dob    = models.DateField ('date of birth')

    address = models.ForeignKey (PLACE, blank=True, null=True)
    contact = models.OneToOneField (CONTACT, blank=True, null=True)
    
    def __unicode__ (self):

        return u'%s %s, %s' % (self.title, self.last, self.first)

class GROUP (models.Model):

    name        = models.CharField (max_length=256)
    description = models.CharField (max_length=256, blank=True, null=True)
    members     = models.ManyToManyField (PERSON, blank=True, null=True,
                      through='ROLE')

    def __unicode__ (self):

        return u'%s' % self.name
    
class ROLE (models.Model):

    person      = models.ForeignKey (PERSON)
    group       = models.ForeignKey (GROUP)
    title       = models.CharField (max_length=256)
    description = models.TextField (blank=True, null=True)
    
    def __unicode__ (self):

        return u'%s in %s' % (self.person, self.group)

class ACTIVITY (models.Model):

    class Meta:

        verbose_name_plural = 'activities'

    name        = models.CharField (max_length=256)
    description = models.TextField (blank=True, null=True)

    def __unicode__ (self):

        return u'%s' % self.name
