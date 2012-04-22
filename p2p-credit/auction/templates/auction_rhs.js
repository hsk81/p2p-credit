// ----------------------------------------------------------------------------
// RHS Panel: gridBidders
// ----------------------------------------------------------------------------

var recordFields = [
    { name : 'id',         mapping : 'id'         }
  , { name : 'first'     , mapping : 'first'      }
  , { name : 'last'      , mapping : 'last'       }
//, { name : 'street'    , mapping : 'street'     }
  , { name : 'city'      , mapping : 'city'       }
  , { name : 'state'     , mapping : 'state'      }
  , { name : 'zip'       , mapping : 'zip'        }
  , { name : 'country'   , mapping : 'country'    }
  , { name : 'amount'    , mapping : 'amount'     }
  , { name : 'cum_amount', mapping : 'cum_amount' }
  , { name : 'rate'      , mapping : 'rate'       }
  , { name : 'status'    , mapping : 'status'     }
];

var remoteJsonStore = new Ext.data.JsonStore({
    fields        : recordFields,
    url           : bid.url_set
        + String.format ("?user-id={0}", user.id)
        + String.format ("&auction-id={0}", auction.id),
    totalProperty : 'totalCount',
    root          : 'records',
    id            : 'remoteStoreId',
    autoLoad      : false,
    remoteSort    : true
});

var renderStatus = function (status) {

    var urlIcon = undefined

    switch (status) {
        case 'tick':
            urlIcon = css2url('icon-tick')
            break;

        case 'tick-last':
            urlIcon =  css2url('icon-check_error')
            break;

        case 'cross':
            urlIcon =  css2url('icon-cross')
            break;

        default:
            urlIcon =  css2url('icon-error')
    }

    return String.format ('<img src="{0}"/ style="cursor: pointer;">', urlIcon)
}

//var stylizeAddress = function (street, column, record) {
//    var city  = record.get('city');
//    var state = record.get('state');
//    var zip   = record.get('zip');
//
//    if (street && zip && city && state) {
//        res = String.format('{0}<br />{1} {2}, {3}', street, zip, city, state);
//    } else
//    if (zip && city && state) {
//        res = String.format('{0} {1}, {2}', zip, city, state);
//    } else {
//        res = '';
//    }
//
//    return res;
//}

var columnModel = [{
    header    : 'ID'
  , dataIndex : 'id'
  , sortable  : true
  , width     : 25
  , resizable : false
  , hidden    : true
  , renderer  : function (id) {
       return String.format ('<span style="color: #0000FF;">{0}</span>', id)
    }
},{
    id        : 'lastColId'
  , header    : 'Last Name'
  , dataIndex : 'last'
  , sortable  : true
  , hideable  : false
  , width     : 75
},{
    id        : 'firstColId'
  , header    : 'First Name'
  , dataIndex : 'first'
  , sortable  : true
  , hideable  : false
  , width     : 75
},{
//    header    : 'Address',
//    dataIndex : 'street',
//    sortable  : false,
//    renderer  : stylizeAddress,
//    width     : 125
//},{
    header    : 'ZIP'
  , dataIndex : 'zip'
  , sortable  : true
  , hidden    : true
  , width     : 75
},{
    header    : 'City'
  , dataIndex : 'city'
  , sortable  : true
  , width     : 100
},{
    header    : 'State'
  , dataIndex : 'state'
  , sortable  : true
  , hidden    : true
  , width     : 50
},{
    header    : 'Country'
  , dataIndex : 'country'
  , sortable  : true
  , width     : 100
},{
    header    : 'Amount'
  , dataIndex : 'amount'
  , sortable  : true
  , width     : 50
},{
    header    : 'Cum. Amount'
  , dataIndex : 'cum_amount'
  , sortable  : true
  , width     : 75
},{
    header    : 'Rate [%]'
  , dataIndex : 'rate'
  , sortable  : true
  , width     : 50
  , renderer  : function (rate) {
        return Number (rate).toFixed (2)
    }
},{
    header    : 'Status'
  , dataIndex : 'status'
  , sortable  : false
  , width     : 50
  , renderer  : renderStatus
  , align     : 'center'
}];

var pagingToolbar = {
    xtype       : 'paging'
  , id          : 'pagingGridBidsId'
  , store       : remoteJsonStore
  , pageSize    : 50
  , displayInfo : true
  , selectInfo  : {ref: 0}

  , taskProgress: {
        interval: 125
      , run: function (index) {
           Ext.MessageBox.updateProgress((index % 9) / 8.0)
        }
    }

  , listeners : {

        change: function (ptb, page_data) {
            if (ptb.selectInfo.ref > 0) {
                var grid =  Ext.getCmp ('gridBidsId')
                var sm = grid.getSelectionModel ()
                var idx = ptb.selectInfo.row
                sm.selectRange (idx, idx)

                Ext.getCmp('tblAuctionId').fireEvent ('refresh')
                Ext.getCmp('tblStatisticsId').fireEvent ('refresh')

                ptb.selectInfo.ref = ptb.selectInfo.ref - 1
            }
        }

      , select: function (id) {
            var grid =  Ext.getCmp ('gridBidsId')
            var ptb = Ext.getCmp ('pagingGridBidsId')

            Ext.Ajax.request ({
                success: function (xhr, opts) {
                    var result = Ext.decode(xhr.responseText);

                    ptb.selectInfo = result.page_info
                    ptb.selectInfo.ref = 1
                    ptb.changePage (ptb.selectInfo.index + 1);
                    
                    Ext.TaskMgr.stop (ptb.taskProgress)
                    Ext.MessageBox.hide ()
                }

              , failure: function (xhr, opts) {
                    Ext.TaskMgr.stop (ptb.taskProgress)
                    Ext.MessageBox.hide ()
                    Ext.MessageBox.show ({
                        title         : 'Error'
                      , msg           : xhr.responseText
                      , closable      : false
                      , width         : 256
                      , buttons       : Ext.MessageBox.OK
                    }) //@TODO!
                }

              , url: bid.url_page.replace ("$0", id)
                    + String.format ("?user-id={0}", user.id)
                    + String.format ("&auction-id={0}", auction.id)
                    + String.format ("&page-size={0}", ptb.pageSize)
                    + String.format ("&sort={0}", grid.sortInfo.field)
                    + String.format ("&dir={0}", grid.sortInfo.direction)
            })

            Ext.MessageBox.show ({
                title         : 'Please wait'
              , msg           : 'Bid has been submitted!'
              , progressText  : 'Updating list ..'
              , progress      : true
              , closable      : false
              , width         : 256
            })

            Ext.TaskMgr.start (this.taskProgress)
        }
        
    }
}

var gridBids = {
    xtype            : 'grid'
  , id               : 'gridBidsId'
  , title            : 'Bids\' List'
  , columns          : columnModel
  , store            : remoteJsonStore
  , loadMask         : true
  , bbar             : pagingToolbar
  , autoExpandColumn : 'lastColId'
  , stripeRows       : true

  , tools:[{
        id:'help'
      , handler: function(event, toolEl, panel) {
            //@TODO!
      }
  }]

  , sortInfo : {
      field     : 'rate'
    , direction : 'ASC'
  }

  , listeners : {

        sortchange : function (grid, sortInfo) {
            grid.sortInfo = sortInfo
        }

      , viewready : function (pnl) {
            Ext.StoreMgr.get('remoteStoreId').load ({
                params : {
                    start : 0,
                    limit : 50
                }
            });

            Ext.getCmp('tblAuctionId').fireEvent ('refresh')
            Ext.getCmp('tblStatisticsId').fireEvent ('refresh')
        }
    }
}

// ----------------------------------------------------------------------------
// RHS Panel
// ----------------------------------------------------------------------------

var pnlRhs = {

    layout : 'border'
  , frame  : true

  , items : [{
        region       : 'north'
      , split        : true
      , height       : 256
      , minHeight    : 256
      , collapsed    : true
      , collapseMode : 'mini'
      , hidden       : true

      , bodyStyle    : 'background-color: white;'
      , layout       : 'fit'
      
      , items : [{
            layout       : 'hbox'
          , layoutConfig : {
                align : 'middle', pack: 'center'
          }

          , items : [{
                width  : 128
              , height : 128
              , html   : '<img \
                    src="{{ MEDIA_URL }}pic/mid/under_construction.jpg">'
          }]
      }]

  },{
        region : 'center'
      , layout : 'fit'
      , items  : [gridBids]
  }]

}
