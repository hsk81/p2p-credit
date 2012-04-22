// ----------------------------------------------------------------------------
// LHS Panel
// ----------------------------------------------------------------------------

/**
 * Tab: Project ---------------------------------------------------------------
 */

var pnlProject = {
    id         : 'pnlProjectId'
  , bodyStyle  : 'padding: 10; text-align: justify'
  , autoScroll : true
  , pid        : 0
}

var tabProject = new Ext.Panel ({
    id     : 'tabProjectId'
  , title  : 'Project'
  , layout : 'fit'
  , items  : [pnlProject]

  , listeners: {

        set_project: function (pid) {
            var pnlProject = Ext.getCmp('pnlProjectId')
            pnlProject.el.mask('Please wait', 'x-mask-loading')

            Ext.Ajax.request({
                url: String.replace (project.url,"$0",pid) + "?in=description"

              , success: function (xhr, opts) {
                    var pnlProject = Ext.getCmp('pnlProjectId');
                    var result     = Ext.decode(xhr.responseText);
                    var project    = map2obj (result).fields;

                    pnlProject.update ({
                        html: project.description
                    });

                    pnlProject.pid = pid
                    pnlProject.el.unmask ();
                },

                failure: function (xhr, opts) {
                    pnlProject.el.unmask ();
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
});

/**
 * Tab: Team ------------------------------------------------------------------
 */

var pnlTeam = {
    id         : 'pnlTeamId'
  , bodyStyle  : 'padding: 10; text-align: justify'
  //autoScroll : true
  , layout     : 'fit'
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
    id     : 'tabTeamId'
  , title  : 'Team'
  , layout : 'fit'
  , items  : [pnlTeam]
}

/**
 * ----------------------------------------------------------------------------
 */

var pnlLhs = new Ext.TabPanel({

    activeTab       : 0
  , enableTabScroll : true
  , tabPosition     : 'top'

  , items           : [
         tabProject
       , tabTeam
    ]

});
