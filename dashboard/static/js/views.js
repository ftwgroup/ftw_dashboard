(function(){
    Backbone.View.prototype.close = function() {
        if (this.beforeClose) {
            this.beforeClose();
        }
        this.undelegateEvents();
        this.remove();
    };

    app.views.Panel = Backbone.View.extend({
        title: "Generic Panel",

        className: "panel",

        initialize: function(options) {
            this.name = options.name;
            this.template = Handlebars.compile(app.utils.templateLoader.get(this.name));
        },

        render: function() {
            var context = this.get_context();
            this.$el.html(this.template(context));
            return this;
        },

        get_context: function() {
            return {};
        },
    }),

    app.views.HomePanel = app.views.Panel.extend({
        title: "Home",
    }),

    app.views.PitchesPanel = app.views.Panel.extend({
        title: "Pitches",
    }),

    app.views.MainView = Backbone.View.extend({
        // The main view consists of a menu and a main panel. Each menu item
        // corresponds to a possible panel.

        el: '#main',
        panel_el: '#panel_holder',
        menu_el: '#menu',

        initialize: function() {
            this.menu_template = Handlebars.compile(app.utils.templateLoader.get('menu'));
            this.panels = {
                'home': new app.views.HomePanel({ name: 'home' }),
                'pitches': new app.views.PitchesPanel({ name: 'pitches' }),
            };
            this.activePanel = this.panels['home'];
        },

        renderMenu: function() {
            var context = {
                panels: this.panels,
                activePanel: this.activePanel,
            };
            $(this.menu_el).html(this.menu_template(context));
        },

        renderPanel: function() {
            if (this.activePanel) {
                $(this.panel_el).html(this.activePanel.render().el);
            }
        },

        render: function() {
            this.renderMenu();
            this.renderPanel();
            return this;
        },

        switchPanel: function(name) {
            if (this.activePanel) {
                this.activePanel.close();
            }
            this.activePanel = this.panels[name];
            this.render();
        }
    });
}).call(this);
