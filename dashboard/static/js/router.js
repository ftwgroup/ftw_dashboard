(function(){
    app.Router = Backbone.Router.extend({
        routes: {
            '': 'home',
            'home': 'home',
            'contacts': 'contactList',
            'contacts/:id': 'contactDetail',
            'pitches': 'pitchList',
            'pitches/:id': 'pitchDetail',
        },

        initialize: function() {
            this.currentPage = null;
            this.mainView = new app.views.MainView({
                pitches: new app.models.PitchList(),
                contacts: new app.models.ContactList()
            }).render();
        },

        home: function() {
            this.mainView.switchPanel('home');
        },

        contactList: function() {
            this.mainView.switchPanel('contacts').showList();
        },

        contactDetail: function(id) {
            this.mainView.switchPanel('contacts').showDetail(id);
        },

        pitchList: function() {
            this.mainView.switchPanel('pitches').showList();
        },

        pitchDetail: function(id) {
            this.mainView.switchPanel('pitches').showDetail(id);
        },

    });

    // Load all Handlebars templates here.
    app.utils.templateLoader.load(['menu', 'home', 'pitches', 'googledrive'], function() {
        new app.Router();
        Backbone.history.start();
    });
}).call(this);
