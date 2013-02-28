(function(){
    Backbone.View.prototype.close = function() {
        if (this.beforeClose) {
            this.beforeClose();
        }
        this.undelegateEvents();
        this.remove();
    };

    // Generic template view.
    app.views.TemplateView = Backbone.View.extend({
        // One of the following should be non-empty: template_name if loading
        // the template from an external file, template_string if the template
        // is defined directly.
        template_name: '',
        template_string: '',

        // String or function containing context for the template.
        context: function() {},

        initialize: function() {
            _(this).bindAll('context');
            if (this.template_string) {
                this.template = Handlebars.compile(_.result(this, 'template_string'));
            } else if (this.template_name) {
                this.template = Handlebars.compile(app.utils.templateLoader.get(this.template_name));
            } else {
                console.log("Error: no template defined for", this);
            }
            this._rendered = false;
        },

        render: function() {
            var context = _.result(this, 'context');
            this.$el.html(this.template(context));
            this._rendered = true;
            return this;
        },

        beforeClose: function() {
            this._rendered = false;
        },
    });

    // Generic panel within the MainView.
    app.views.Panel = Backbone.View.extend({
        className: "panel",
        title: "Generic Panel",

        initialize: function(options) {
            this.name = options.name;
        },
    });

    app.views.HomePanel = app.views.Panel.extend({
        title: "Home",

        render: function() {
            this.$el.html("Home.");
            return this;
        },
    });

    // An individual pitch item in a PitchListView.
    var PitchItemView = app.views.TemplateView.extend({
        template_string: '<div class="pitch-item"><a class="pitch-item-link" href="#pitches/{{id}}">{{snippet}}</a></div>',

        initialize: function() {
            app.views.TemplateView.prototype.initialize.apply(this, arguments);
            _.bindAll(this, 'change', 'context');
            this.model.on('change', this.change);
        },

        change: function() {
            this._rendered && this.render();
        },

        context: function() {
            return {
                'id': this.model.get('id'),
                'snippet': this.model.get('snippet'),
            };
        },
    });

    // A list of pitch items.
    var PitchListView = Backbone.View.extend({
        initialize: function() {
            this._item_views = [];
            this._rendered = false;
            _.bindAll(this, 'add', 'remove', 'reset');
            this.collection.on('add', this.add);
            this.collection.on('remove', this.remove);
            this.collection.on('reset', this.reset);
            this.reset();
        },

        add: function(pitch) {
            var view = new PitchItemView({ model: pitch });
            this._item_views.push(view);

            if (this._rendered) {
                this.$el.append(view.render().el);
            }
        },

        remove: function(pitch) {
            var dead_view = _(this._item_views).select(function(view) {
                return view.model === pitch;
            })[0];
            if (dead_view) {
                this._item_views = _(this._item_views).without(dead_view);
                if (this._rendered) {
                    deadview.$el.remove();
                }
                dead_view.close();
            }
        },

        reset: function() {
            this._item_views = [];
            var self = this;
            this.collection.each(function(pitch) {
                var view = new PitchItemView({ model: pitch });
                self._item_views.push(view);
            });

            this._rendered && this.render();
        },

        render: function() {
            this.$el.empty();
            var self = this;
            _(this._item_views).each(function(view) {
                self.$el.append(view.render().el);
            });
            this._rendered = true;
            return this;
        },
    });

    // A detail view for a single pitch.
    var PitchDetailView = app.views.TemplateView.extend({
        template_string: '<h3 class="pitch-detail-snippet">{{snippet}}</h3><p class="pitch-detail-description">{{description}}</p>',

        initialize: function() {
            app.views.TemplateView.prototype.initialize.apply(this, arguments);
            _.bindAll(this, 'change');
            this.model.on('change', this.change);
        },

        change: function() {
            this._rendered && this.render();
        },

        context: function() {
            return {
                'id': this.model.get('id'),
                'snippet': this.model.get('snippet'),
                'description': this.model.get('description'),
                'image': this.model.get('image'),
            };
        },
    });

    app.views.PitchesPanel = app.views.Panel.extend({
        title: "Pitches",

        initialize: function(options) {
            app.views.Panel.prototype.initialize.apply(this, arguments);

            // Fetch list of pitches from the server.
            this.collection.fetch();

            this.view_stack = [];
        },

        render: function() {
            var active = _(this.view_stack).last();
            if (active) {
                this.$el.html(active.view.render().el);
            }
            return this;
        },

        showList: function() {
            var last = _(this.view_stack).last() || {};
            this.view_stack.push({
                path: '#pitches',
                view: new PitchListView({ collection: this.collection, back: last.path }),
            });
            return this.render();
        },

        showDetail: function(id) {
            var last = _(this.view_stack).last() || {};
            var pitch = this.collection.get(id);
            this.view_stack.push({
                path: '#pitches/' + id,
                view: new PitchDetailView({ model: pitch, back: last.path }),
            });
            return this.render();
        },
    });

    app.views.MainView = Backbone.View.extend({
        // The main view consists of a menu and a main panel. Each menu item
        // corresponds to a possible panel.

        el: '#main',
        panel_el: '#panel_holder',
        menu_el: '#menu',

        initialize: function(options) {
            this.menu_template = Handlebars.compile(app.utils.templateLoader.get('menu'));
            this.panels = {
                'home': new app.views.HomePanel({ name: 'home' }),
                'pitches': new app.views.PitchesPanel({ name: 'pitches', collection: options.pitches }),
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
            if (!this.activePanel || this.activePanel.name !== name) {
                this.activePanel && this.activePanel.close();
                this.activePanel = this.panels[name];
                this.render();
            }
            return this.activePanel;
        }
    });
}).call(this);
