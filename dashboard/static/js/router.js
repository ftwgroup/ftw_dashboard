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

    // Setup for Django's CSRF protection.
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    var csrftoken = $.cookie('csrftoken');
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Load all Handlebars templates here.
    app.utils.templateLoader.load(['menu', 'home', 'pitches', 'googledrive'], function() {
        new app.Router();
        Backbone.history.start();
    });
}).call(this);
