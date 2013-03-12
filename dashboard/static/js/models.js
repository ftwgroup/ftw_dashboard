(function(){
    app.models.GoogleDrive = Backbone.Collection.extend({
        url: '/dashboard/googledrive',

        initialize: function() {
            this.api_loading = $.Deferred();
            var self = this;
            gapi.client.load('drive', 'v2', function() {
                self.api_loading.resolve();
            });
        },

        fetch: function() {
            var fetching = $.Deferred();
            this.api_loading.done(function() {
                var request = gapi.client.drive.files.list();
                request.execute(function(response) {
                    fetching.resolve(response);
                });
            });

            var self = this;
            fetching.done(function(response) {
                console.log("GoogleDrive list response:", response);
                self.reset(response.items);
            });
            return fetching;
        },
    });

    app.models.Pitch = Backbone.Model.extend({
        initialize: function() {
        },
    });

    app.models.PitchList = Backbone.Collection.extend({
        model: app.models.Pitch,
        url: '/dashboard/pitches',
    });

}).call(this);
