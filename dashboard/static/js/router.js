(function(){
    app.Router = Backbone.Router.extend({
        routes: {
            '': 'home',
            'home': 'home',
            'pitches': 'pitchList',
            'pitches/:id': 'pitchDetail',
        },

        initialize: function() {
            this.currentPage = null;
            this.mainView = new app.views.MainView({
                pitches: new app.models.PitchList(),
            }).render();
        },

        home: function() {
            this.mainView.switchPanel('home');
        },

        pitchList: function() {
            this.mainView.switchPanel('pitches').showList();
        },

        pitchDetail: function(id) {
            this.mainView.switchPanel('pitches').showDetail(id);
        },

    });

    // Load all Handlebars templates here.
    app.utils.templateLoader.load(['menu', 'home', 'pitches'], function() {
        new app.Router();
        Backbone.history.start();
    });
}).call(this);
