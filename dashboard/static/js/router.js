(function(){
    app.Router = Backbone.Router.extend({
        routes: {
            '': 'goHome',
            'home': 'goHome',
            'pitches': 'goPitches',
        },

        initialize: function() {
            this.currentPage = null;
            this.mainView = new app.views.MainView().render();
        },

        goHome: function() {
            this.mainView.switchPanel('home');
        },

        goPitches: function() {
            this.mainView.switchPanel('pitches');
        }

    });

    app.utils.templateLoader.load(['menu', 'home', 'pitches'], function() {
        new app.Router();
        Backbone.history.start();
    });
}).call(this);
