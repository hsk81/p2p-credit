from django.conf.urls.defaults import *
from django.contrib            import admin
from views                     import DATA

admin.autodiscover()

urlpatterns = patterns('',

    (r'^svc/'     , include('svc.urls'     , namespace='svc'     )),
    (r'^people/'  , include('people.urls'  , namespace='people'  )),
    (r'^org/'     , include('org.urls'     , namespace='org'     )),
    (r'^com/'     , include('com.urls'     , namespace='com'     )),
    (r'^edu/'     , include('edu.urls'     , namespace='edu'     )),
    (r'^project/' , include('prj.urls'     , namespace='prj'     )),
    (r'^auction/' , include('auction.urls' , namespace='auction' )),

  # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

  # url(
  #     r'^$', 
  #     direct_to_template, 
  #     {'template': 'base.html',
  #      'extra_context': {} 
  #     },
  #     name="base"
  # ),

    url (
        r'^json/info/$',
        DATA.info,
        name='json.info'
    ),

)

