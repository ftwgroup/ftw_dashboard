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

}).call(this);
