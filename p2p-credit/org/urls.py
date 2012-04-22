from django.conf.urls.defaults   import *
from django.views.generic.simple import direct_to_template

from views import DATA
from views import POST

urlpatterns = patterns('',

  # url(
  #     r'^$',
  #     direct_to_template,
  #     {'template': 'org.html',
  #      'extra_context': {}
  #     },
  #     name='people'
  # ),

    url(
        r'^json/info/$',
        DATA.info,
        name='json.info'
    ),

)

if __name__ == "__main__":

    pass

else:

    from svc.urls import data_urlpatterns
    from models   import *

    urlpatterns += data_urlpatterns (ORGANIZATION)
    urlpatterns += data_urlpatterns (SERVICE)
    urlpatterns += data_urlpatterns (B2C_SERVICE)
    urlpatterns += data_urlpatterns (B2B_SERVICE)
