(function(){
    app.utils.templateLoader = {
        templates: {},
        load: function(names, callback) {
            var deferreds, _this = this;
            deferreds = [];
            $.each(names, function(index, name) {
                return deferreds.push($.get('js/templates/' + name + '.hb', function(data) {
                    console.log('loaded');
                    return _this.templates[name] = data;
                }));
            });
            return $.when.apply(null, deferreds).done(callback);
        },
        get: function(name) {
            var template;
            template = this.templates[name];
            if (!template) {
                console.log('Template not loaded', 'Error');
            }
            return template;
        }
    };
}).call(this);
