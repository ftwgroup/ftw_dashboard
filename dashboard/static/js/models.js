(function(){
    app.models.GoogleDrive = Backbone.Collection.extend({
        url: '/dashboard/googledrive',
    });

    app.models.Pitch = Backbone.Model.extend({
        initialize: function() {
        },
    });

    app.models.PitchList = Backbone.Collection.extend({
        model: app.models.Pitch,
        url: '/dashboard/pitches',
    });

    app.models.Contact = Backbone.Model.extend({
        initialize: function() {
        },
        parse: function(response) {
            response['id'] = response.uid;
            console.log('response', response);
            return response
        }
    });

    app.models.ContactList = Backbone.Collection.extend({
        model: app.models.Contact,
        url: '/contacts'
    });

}).call(this);
