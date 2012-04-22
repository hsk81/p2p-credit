// ----------------------------------------------------------------------------
// PRJ Panel
// ----------------------------------------------------------------------------

var recordFields = [
    { name : 'id',          mapping : 'id'          }
  , { name : 'name',        mapping : 'name'        }
  , { name : 'description', mapping : 'description' }
  , { name : 'contact',     mapping : 'contact'     }
  , { name : 'start_date',  mapping : 'start_date'  }
  , { name : 'end_date',    mapping : 'end_date'    }
];

var remoteJsonStore = new Ext.data.JsonStore({
    fields        : recordFields
  , url           : project_set.url
  , totalProperty : 'totalCount'
  , root          : 'records'
  , id            : 'remoteStoreId'
  , autoLoad      : true
  , remoteSort    : true
});

var renderIcon = function () {

    var urlIcon = css2url ('icon-information')
    var imgIcon = String.format (
        '<img src="{0}"/ style="cursor: pointer;">',
        urlIcon
    )

    return imgIcon
}

var columnModel = [{
    header    : 'ID'
  , dataIndex : 'id'
  , sortable  : true
  , width     : 25
  , resizable : false
  , hidden    : true
  , renderer  : function (id) {
        return '<span style="color: #0000FF;">' + id + '</span>';
  }
},{
    header    : 'Info'
  //dataIndex : ''
  , sortable  : false
  , width     : 50
  , renderer  : renderIcon
  , align     : 'center'
},{
    id        : 'nameColId'
  , header    : 'Name'
  , dataIndex : 'name'
  , sortable  : true
  , hideable  : false
  , width     : 75
},{
    id        : 'descriptionColId'
  , header    : 'Description'
  , dataIndex : 'description'
  , sortable  : false
  , hideable  : false
},{
    id        : 'contactColId'
  , header    : 'Contact'
  , dataIndex : 'contact'
  , sortable  : true
  , hideable  : false
  , width     : 150
},{
    id        : 'startDateColId'
  , header    : 'Start Date'
  , dataIndex : 'start_date'
  , sortable  : true
  , hideable  : false
  , width     : 75
},{
    id        : 'endDateColId'
  , header    : 'End Date'
  , dataIndex : 'end_date'
  , sortable  : true
  , hideable  : false
  , width     : 75
}]

var pagingToolbar = {

    xtype       : 'paging'
  , id          : 'pagingGridBidsId'
  , store       : remoteJsonStore
  , pageSize    : 50
  , displayInfo : true

}

var pnlPrj = {

    title            : 'Projects\' List'
  , id               : 'gridProjectsId'
  , xtype            : 'grid'
  , columns          : columnModel
  , store            : remoteJsonStore
  , loadMask         : true
  , bbar             : pagingToolbar
  , autoExpandColumn : 'descriptionColId'
  , stripeRows       : true
  
  , tools :[{
        id      :'help',
        handler : function(event, toolEl, panel) {
            //@TODO!
        }
    }]

  , listeners: {
        rowclick: function (grid, idx, e) {
            var row = grid.store.getAt (idx)
            var pid = row.get ("id")            
            Ext.getCmp ('gridAuctionsId').fireEvent ('set_project', pid)            
            Ext.getCmp ('tabProjectId').fireEvent ('set_project', pid)
        }

      , viewready : function (pnl) {
            var grid =  Ext.getCmp ('gridProjectsId')
            var sm = grid.getSelectionModel ()
            sm.selectRange (0, 0)
            grid.fireEvent ('rowclick', grid, 0, null)
        }
  }
}
