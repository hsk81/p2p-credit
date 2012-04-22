// ----------------------------------------------------------------------------
// RHS Panel
// ----------------------------------------------------------------------------

var recordFields = [
    { name : 'id'            , mapping : 'id'            }
  , { name : 'is_active'     , mapping : 'is_active'     }
  , { name : 'start_date'    , mapping : 'start_date'    }
  , { name : 'expiry_date'   , mapping : 'expiry_date'   }
  , { name : 'target_amount' , mapping : 'target_amount' }
  , { name : 'actual_amount' , mapping : 'actual_amount' }
  , { name : 'target_rate'   , mapping : 'target_rate'   }
  , { name : 'actual_rate'   , mapping : 'actual_rate'   }
];

var remoteJsonStore = new Ext.data.JsonStore ({
    fields        : recordFields
  , url           : auction_set.url
  , totalProperty : 'totalCount'
  , root          : 'records'
  , autoLoad      : true
  , remoteSort    : true
});

var renderIsActive = function (is_active) {

    var urlIcon = (is_active)
        ? css2url('icon-bell')
        : css2url('icon-bell_silver')

    return String.format ('<img src="{0}"/ style="cursor: pointer;">', urlIcon)
}

var columnModel = [{
    header    : 'ID'
  , dataIndex : 'id'
  , sortable  : true
  , width     : 25
  , resizable : false
  , hidden    : true
  , renderer  : function (id) {
        return '<span style="color: #0000FF;">' + id + '</span>'
  }
},{
    header    : 'Active'
  , dataIndex : 'is_active'
  , sortable  : false
  , width     : 50
  , renderer  : renderIsActive
  , align     : 'center'
},{
    id        : 'startDateColId'
  , header    : 'Start Date'
  , dataIndex : 'start_date'
  , sortable  : true
  , hideable  : false
  , width     : 75
},{
    id        : 'expiryDateColId'
  , header    : 'Expiry Date'
  , dataIndex : 'expiry_date'
  , sortable  : true
  , hideable  : false
  , width     : 75
},{
    id        : 'targetAmountColId'
  , header    : 'Target Amount'
  , dataIndex : 'target_amount'
  , sortable  : true
  , hideable  : false
  , width     : 100
},{
    id        : 'targetRateColId'
  , header    : 'Target Rate'
  , dataIndex : 'target_rate'
  , sortable  : true
  , hideable  : false
  , width     : 100
},{
    id        : 'actualAmountColId'
  , header    : 'Actual Amount'
  , dataIndex : 'actual_amount'
  , sortable  : true
  , hideable  : false
  , width     : 100
},{
    id        : 'actualRateColId'
  , header    : 'Actual Rate'
  , dataIndex : 'actual_rate'
  , sortable  : true
  , hideable  : false
  , width     : 100
}]

var pnlRhs = new Ext.grid.GridPanel ({

    title            : 'Auctions\' List'
  , id               : 'gridAuctionsId'
  , columns          : columnModel
  , store            : remoteJsonStore
  , loadMask         : true
  //bbar             : pagingToolbar
  , autoExpandColumn : 'targetAmountColId'
  , stripeRows       : true

  , tools : [{
        id      :'help',
        handler : function (event, toolEl, panel) {
            //@TODO!
        }
  }]

  , listeners: {

        rowclick: function (grid, idx, event) {
            var row = grid.store.getAt (idx)            
            var url = String.replace (auction.url_view, "$0", row.get ("id"))
                    + window.location.search

            open (url)
        }

      , set_project: function (id) {
            this.store.proxy.conn.url = auction_set.url +
                String.format ("?project-id={0}", id);
            this.store.load ();            
        }
    }
});
