(function(){
    window.app = {
        models: {},
        views: {},
        utils:{}
    };
    Backbone.View.prototype.close = function() {
        if (this.beforeClose) {
            this.beforeClose();
        }

        this.undelegateEvents();
        this.remove();
    };

    app.Router = Backbone.Router.extend({
        routes: {
            '': 'home'
        },

        initialize: function() {
            this.currentPage = null;
        },

        home: function() {
            this.currentPage = new app.views.MainView().render();
        }

    });
}).call(this);
