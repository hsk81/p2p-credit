// ----------------------------------------------------------------------------
// LHS Panel: top part
// ----------------------------------------------------------------------------

var frmTop = {

    height       : 58
  , width        : "100%"
  , bodyStyle    : 'padding: 5;'

  , layout       : 'form'
  , labelWidth   : 56
  , defaultType  : 'field'

  , items        : [{
        fieldLabel : '<b>Project</b>'
      , anchor     : '100%'
      , readOnly   : true
      , value      : project.string
    },{
        fieldLabel : '<b>Contact</b>'
      , anchor     : '100%'
      , readOnly   : true
      , value      : project.contact.string
    }]

}

var picTop = {

    layout : 'vbox'
  , layoutConfig : {
        align : 'stretch'
  }

  , bodyStyle : 'padding: 0 0 5 0'
  , items : [{
        flex : 1
      , bodyStyle : 'border: 2px solid black; background-color: ghostwhite'
      /*html  : '<img \
        src="{{ MEDIA_URL }}ico/crystal/64x64/apps/personal.png" >'*/
  }]


}

var pnlTop = {

    height : 58

  , layout : 'hbox'
  , layoutConfig : {
        align : 'stretch'
  }

  , items : [{
        flex   : 1
      , items  : [frmTop]
  }/*,{
        width  : 64
      , layout : 'fit'
      , items  : [picTop]
  }*/]

}

// ----------------------------------------------------------------------------
// LHS Panel: mid part
// ----------------------------------------------------------------------------

/**
 * Tab: Information -----------------------------------------------------------
 */

var tblBorrower = new Ext.grid.PropertyGrid({

    id : 'tblBorrowerId'
  , stripeRows: true
  , autoHeight: true

  , viewConfig : {
        scrollOffset    : 0
      , forceFit        : true
      , headersDisabled : true
    }

  , propertyNames: {
        f00_title      : 'Title'
      , f01_first      : 'First Name'
      , f02_last       : 'Last Name'
      , f03_dob        : 'Date of Birth'
      , f04_address    : 'Address'
      , f05_education  : 'Education'
      , f06_profession : 'Profession'
    }

  , source: {
          f00_title      : project.contact.title
        , f01_first      : project.contact.first
        , f02_last       : project.contact.last
        , f03_dob        : project.contact.dob
        , f04_address    : project.contact.address
        , f05_education  : project.contact.education.string
        , f06_profession : project.contact.profession
    }

  , listeners: {
        beforeedit: function (arg) {
            return false;
        }
    }

});

var tblAuction = new Ext.grid.PropertyGrid({

    id : 'tblAuctionId'
  , stripeRows: true
  , autoHeight: true

  , viewConfig : {
        scrollOffset    : 0
      , forceFit        : true
      , headersDisabled : true
    }

  , propertyNames: {
        f00_targetAmount : 'Target Amount'
      , f01_targetRate   : 'Target Rate [%]'
      , f02_actualAmount : 'Actual Amount'
      , f03_actualRate   : 'Actual Rate [%]'
      , f04_startDate    : 'Start Date'
      , f05_expiryDate   : 'Expiry Date'
    }

  , source: {
        f00_targetAmount : auction.target_amount
      , f01_targetRate   : auction.target_rate
      , f02_actualAmount : auction.actual_amount
      , f03_actualRate   : auction.actual_rate
      , f04_startDate    : auction.start_date
      , f05_expiryDate   : auction.expiry_date
    }

  , listeners: {
        beforeedit: function (arg) {
            return false;
        }

      , refresh: function () {
            tblAuction.el.mask ('Please wait', 'x-mask-loading')

            Ext.Ajax.request ({
                url: statistics.url_basic

                    + String.format ("?auction-id={0}", auction.id),

                success: function (xhr, opts) {
                    var auctionInfo = Ext.decode (xhr.responseText)

                    var source = tblAuction.source
                    source.f02_actualAmount = auctionInfo.actual_amount
                    source.f03_actualRate = auctionInfo.actual_rate
                    tblAuction.setSource (source)

                    tblAuction.el.unmask ();
                },

                failure: function (xhr, opts) {
                    tblAuction.el.unmask ()
                    Ext.MessageBox.show ({
                        title         : 'Error'
                      , msg           : xhr.responseText
                      , closable      : false
                      , width         : 256
                      , buttons       : Ext.MessageBox.OK
                    }) //@TODO!
                }
            })
        }

      , viewready : function (grid) {
            grid.fireEvent ('refresh')
      }
    }
    
});

var tblStatistics = new Ext.grid.PropertyGrid({

    id : 'tblStatisticsId'
  , stripeRows: true

  , propertyNames: {
        f00_nob       : '<i>Number of Bids (NOB)</i>'
      , f01_avgNob    : 'Average NOB per Day'
      , f02_minNob    : 'Minimum NOB per Day'
      , f03_maxNob    : 'Maximum NOB per Day'

      , f04_rob       : '<i>Relevant NOB (RNB)</i>'
      , f05_avgRob    : 'Average RNB per Day'
      , f06_minRob    : 'Minimum RNB per Day'
      , f07_maxRob    : 'Maximum RNB per Day'

      , f08_avgRate   : '<i>Weighted Avg. Rate [%]</i>'
      , f09_minRate   : 'Minimum Rate [%]'
      , f10_maxRate   : 'Maximum Rate [%]'

      , f11_sumAmount : '<i>Sum of Amounts</i>'
      , f12_avgAmount : 'Average Amount'
      , f13_minAmount : 'Minimum Amount'
      , f14_maxAmount : 'Maximum Amount'
    }

  , source: {
        f00_nob       : '?'
      , f01_avgNob    : '?'
      , f02_minNob    : '?'
      , f03_maxNob    : '?'

      , f04_rob       : '?'
      , f05_avgRob    : '?'
      , f06_minRob    : '?'
      , f07_maxRob    : '?'

      , f08_avgRate   : '?'
      , f09_minRate   : '?'
      , f10_maxRate   : '?'

      , f11_sumAmount : '?'
      , f12_avgAmount : '?'
      , f13_minAmount : '?'
      , f14_maxAmount : '?'
    }

  , viewConfig : {
        scrollOffset    : 0
      , forceFit        : true
      , headersDisabled : true
    }

  , listeners: {
        beforeedit: function (arg) {
            return false;
        }

      , refresh: function () {
            tblStatistics.el.mask ('Please wait', 'x-mask-loading')

            Ext.Ajax.request({
                url: statistics.url_extended

                    + String.format ("?auction-id={0}", auction.id),

                success: function (xhr, opts) {
                    var statisticsInfo = Ext.decode (xhr.responseText)
                    var source = tblStatistics.source

                    source.f00_nob       = statisticsInfo.nob
                    source.f01_avgNob    = statisticsInfo.avg_nob
                    source.f02_minNob    = statisticsInfo.min_nob
                    source.f03_maxNob    = statisticsInfo.max_nob

                    source.f04_rob       = statisticsInfo.rob
                    source.f05_avgRob    = statisticsInfo.avg_rob
                    source.f06_minRob    = statisticsInfo.min_rob
                    source.f07_maxRob    = statisticsInfo.max_rob

                    source.f08_avgRate   = statisticsInfo.avg_rate
                    source.f09_minRate   = statisticsInfo.min_rate
                    source.f10_maxRate   = statisticsInfo.max_rate

                    source.f11_sumAmount = statisticsInfo.sum_amount
                    source.f12_avgAmount = statisticsInfo.avg_amount
                    source.f13_minAmount = statisticsInfo.min_amount
                    source.f14_maxAmount = statisticsInfo.max_amount

                    tblStatistics.setSource (source)
                    tblStatistics.el.unmask ()
                },

                failure: function (xhr, opts) {
                    tblStatistics.el.unmask () //@TODO!
                }
            })
        }
    }
});

var tabInfo = {
    
    title  : 'Information'
  , layout : 'fit'
  , items  : [{

      autoScroll : true
    , items : [{
            title  : 'Borrower'
          , hidden : true
          , layout : 'fit'
          , items  : [tblBorrower]

          , tools:[{
                id:'help',
                handler: function(event, toolEl, panel) {
                    //@TODO!
                }
            }]

      },{
            title  : 'Auction'
          , layout : 'fit'
          , items  : [tblAuction]

          , tools:[{
                id:'refresh',
                qtip: 'Refresh',
                handler: function(event, toolEl, panel) {
                    tblAuction.fireEvent ('refresh')
                }
            },{
                id:'help',
                handler: function(event, toolEl, panel) {
                    //@TODO!
                }
            }]

      },{
            title  : 'Statistics'
          , layout : 'fit'
          , items  : [tblStatistics]

          , tools:[{
                id:'refresh',
                qtip: 'Refresh',
                handler: function(event, toolEl, panel) {
                    tblStatistics.fireEvent ('refresh')
                }
            },{
                id:'help',
                handler: function(event, toolEl, panel) {
                    //@TODO!
                }
            }]
      }]
  }]
}

/**
 * Tab: Project ---------------------------------------------------------------
 */

var pnlProject = {
    id         : 'pnlProjectId'
  , bodyStyle  : 'padding: 10; text-align: justify'
  , autoScroll : true
  , updated    : false
}

var tabProject = new Ext.Panel ({
    title  : 'Project'
  , layout : 'fit'
  , items  : [pnlProject]

  , listeners: {

        activate: function (tabPanel) {
            var pnlProject = Ext.getCmp('pnlProjectId');
            if (pnlProject.updated != true) {
                
                tabPanel.el.mask ('Please wait', 'x-mask-loading')
                Ext.Ajax.request ({
                    url: project.url + "?in=description",

                    success: function (xhr, opts) {
                        var pnlProject = Ext.getCmp ('pnlProjectId');
                        var result     = Ext.decode (xhr.responseText)
                        var project    = map2obj (result).fields

                        pnlProject.update ({
                            html: project.description
                        });

                        pnlProject.updated = true
                        tabPanel.el.unmask ()
                    },

                    failure: function (xhr, opts) {
                        tabPanel.el.unmask ()
                        Ext.MessageBox.show ({
                            title         : 'Error'
                          , msg           : xhr.responseText
                          , closable      : false
                          , width         : 256
                          , buttons       : Ext.MessageBox.OK
                        }) //@TODO!
                    }
                })
            }
        }
        
    }
});

/**
 * Tab: Team ------------------------------------------------------------------
 */

var pnlTeam = {
    id         : 'pnlTeamId'
  , bodyStyle  : 'padding: 10; text-align: justify'
  //autoScroll : true
  , layout : 'fit'
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
}

var tabTeam = {
    title  : 'Team'
  , layout : 'fit'
  , items  : [pnlTeam]  
}

/**
 * ----------------------------------------------------------------------------
 */

var pnlMid = new Ext.TabPanel({
    
    activeTab       : 0
  , enableTabScroll : true
  , tabPosition     : 'top'

  , items           : [
         tabInfo
       , tabProject
       , tabTeam
    ]

});

// ----------------------------------------------------------------------------
// LHS Panel: low part
// ----------------------------------------------------------------------------

var tbLow = ['->', {
        
    text    : 'Submit'
  , style   : 'padding: 5;'
  , iconCls : 'icon-coins_add'
  , handler : function (btn) {

        var formPanel = Ext.getCmp('formBidId');
        formPanel.el.mask('Please wait', 'x-mask-loading');
        
        function _onSuccess (form, action) {
            formPanel.el.unmask ();
            formPanel.fireEvent ('submitted', action.result.id)
        }

        function _onFailure (form, action) {
            formPanel.el.unmask();

            if (action) {
                switch (action.result.resinfo) {
                    case "AUCTION_EXPIRED":
                        msg = 
                            "Since this auction has already expired, it does " +
                            "not accept any bids anymore. Please select "      +
                            "another auction or project to bid for."
                        break;
                    case "DB_WRITE_ERROR":
                        msg =
                            "Saving the provided bid has failed, since "       +
                            "access to internal database was denied. Please "  +
                            "retry later."
                        break;
                    case "INVALID_INPUT":
                        msg =
                            "The provided input for this bid is invalid. "     +
                            "Please verify provided input and retry again."
                        break;
                    default:
                        msg = 
                            "Saving the provided bid has failed, due to an "   +
                            "unknown reason."
                }
            } else {
                msg = 
                    "Saving the provided bid has failed, due to an "   +
                    "unknown reason."
            }

            Ext.MessageBox.show ({
                title : 'Bidding failed'
              , msg : msg
              , closable : false
              , width : 480
              , buttons : Ext.MessageBox.OK
              , icon : Ext.MessageBox.INFO
            }) //@TOOD: Improve 'design'!

        }

        formPanel.getForm ().submit ({
            url: bid.url_post
                + String.format ("?user-id={0}", user.id)
                + String.format ("&auction-id={0}", auction.id)

          , success : _onSuccess
          , failure : _onFailure
        });

    }
}];

var pnlLow = new Ext.form.FormPanel ({

    height      : 120
  , title       : 'Bidding'
  , border      : true
  , width       : "100%"
  , bodyStyle   : 'padding: 5;'

  , layout      : 'form'
  , id          : 'formBidId'
  , labelWidth  : 64
  , defaultType : 'field'

  , items : [{
        fieldLabel : '<b>Amount</b>'
      , id         : 'fieldAmountId'
      , name       : 'amount'
      , anchor     : '100%'
      , value      : auction.default_bid.amount
    },{
        fieldLabel : '<b>Rate [%]</b>'
      , id         : 'fieldRateId'
      , name       : 'rate'
      , anchor     : '100%'
      , value      : Number (auction.default_bid.rate).toFixed (2)
    }]

  , bbar : tbLow

  , tools : [{
        id:'help',
        handler: function (event, toolEl, panel) {
            //@TODO!
        }
    }]

})

pnlLow.addEvents ({
    'submitted' : true
})

Ext.getCmp ('formBidId').on ('submitted', function (id) {
    Ext.getCmp ('pagingGridBidsId').fireEvent ('select', id);
});

// ----------------------------------------------------------------------------
// LHS Panel
// ----------------------------------------------------------------------------

var pnlLhs = {
    
    layout : 'vbox'
  , layoutConfig : {
      align : 'stretch'
  }

, items : [
        pnlTop
   ,{
        height : 1
  },{
        layout : 'fit'
      , flex   : 1
      , items : [pnlMid]
  },{
        height : 5
  },
        pnlLow
  ]

}
