from django.conf.urls.defaults   import *
from django.views.generic.simple import direct_to_template

from views import VIEW
from views import DATA
from views import POST

urlpatterns = patterns('',

  # url(
  #     r'^$',
  #     direct_to_template,
  #     {'template': 'auction.html',
  #      'extra_context': {}
  #     },
  #
  #     name='auction'
  # ),

    url(
        r'^(?P<id>\d+|\$0)/$',
        VIEW.main,
        name='view.main'
    ),

    url(
        r'^lhs.js$',
        direct_to_template,
        {'template': 'auction_lhs.js',
         'extra_context': {}
        },
        name='lhs.js'
    ),

    url(
        r'^rhs.js$',
        direct_to_template,
        {'template': 'auction_rhs.js',
         'extra_context': {}
        },
        name='rhs.js'
    ),

    url(
        r'^json/info/$',
        DATA.info,
        name='json.info'
    ),

    url(
        r'^json/statistics/basic/$',
        DATA.statistics_basic,
        name='json.statistics.basic'
    ),

    url(
        r'^json/statistics/extended/$',
        DATA.statistics_extended,
        name='json.statistics.extended'
    ),

    url(
        r'^json/auctions-by-project/$',
        DATA.auctions_by_project,
        name='json.auctions_by_project'
    ),

    url(
        r'^post/BID/(?P<id>\d+|\$0)/cache-page/$',
        POST.cache_page,
        name='post.cache_page'
    ),

    url(
        r'^post/BID/$',
        POST.bid,
        name='post.BID'
    ),

)

if __name__ == "__main__":

    pass

else:

    from svc.urls import data_urlpatterns
    from models   import *

    urlpatterns += data_urlpatterns (AUCTION)
    urlpatterns += data_urlpatterns (BID, f_set= {'extjs': DATA.bids})
    