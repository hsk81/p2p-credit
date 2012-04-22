from django.conf.urls.defaults   import *
from django.views.generic.simple import direct_to_template

from views import VIEW
from views import DATA
from views import POST

urlpatterns = patterns('',

  # url(
  #     r'^$',
  #     direct_to_template,
  #     {'template': 'prj.html',
  #      'extra_context': {}
  #     },
  #     name='people'
  # ),

    url(
        r'^all/$',
        VIEW.main,
        name='view.main'
    ),

    url(
        r'^all.js$',
        direct_to_template,
        {'template': 'prj_all.js',
         'extra_context': {}
        },
        name='all.js'
    ),

    url(
        r'^lhs.js$',
        direct_to_template,
        {'template': 'prj_lhs.js',
         'extra_context': {}
        },
        name='lhs.js'
    ),

    url(
        r'^rhs.js$',
        direct_to_template,
        {'template': 'prj_rhs.js',
         'extra_context': {}
        },
        name='rhs.js'
    ),

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

    urlpatterns += data_urlpatterns (PROJECT, f_set={'extjs' : DATA.projects})
