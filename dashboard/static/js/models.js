(function(){
    app.models.GoogleDrive = Backbone.Collection.extend({
        initialize: function() {
            // Load the Drive API.
            this.api_loading = $.Deferred();
            var self = this;
            gapi.client.load('drive', 'v2', function() {
                self.api_loading.resolve();
            });
        },

        fetch: function() {
            if (this.fetching) {
                // Fetching in progress. Ignore this request.
                return;
            }

            // Fetch the user's file list after the API is loaded.
            this.fetching = $.Deferred();
            var self = this;
            this.api_loading.done(function() {
                var request = gapi.client.drive.files.list();
                request.execute(function(response) {
                    console.log("Fetched Google Drive file list.");
                    self.fetching.resolve(response);
                    self.fetching = null;
                    self.reset(response.items);
                });
            });

            return this.fetching;
        },
    });

    app.models.GoogleAuthCredentials = Backbone.Model.extend({
        url: '/dashboard/google-auth-credentials/',

        initialize: function(options) {
            this.set('access_token', options.access_token);
            this.set('expires_at', options.expires_at);
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
