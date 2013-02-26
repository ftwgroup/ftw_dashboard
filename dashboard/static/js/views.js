(function(){
    app.views.SubView = Backbone.View.extend({
        //something
    }),
    app.views.MainView = Backbone.View.extend({

        events: {
            'click': 'showSubView'
        },

        initialize: function() {
            this.template = Handlebars.compile(app.utils.templateLoader.get('main'));
            this.currentSubView = null;
        },

        render: function() {
            $(this.el).append(this.template());
            return this;
        },

        showSubView: function() {
            if (this.currentSubView) {
                this.currentSubView.close();
                this.currentSubView = new SubView().render();
            } else {
                this.currentSubView = new SubView().render();
            }
        }
    });
}).call(this);
