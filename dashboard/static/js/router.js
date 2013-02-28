(function(){
    app.Router = Backbone.Router.extend({
        routes: {
            '': 'home',
            'home': 'home',
            'pitches': 'pitches',
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

        pitches: function() {
            this.mainView.switchPanel('pitches');
        },

    });

    app.utils.templateLoader.load(['menu', 'home', 'pitches'], function() {
        new app.Router();
        Backbone.history.start();
    });
}).call(this);
