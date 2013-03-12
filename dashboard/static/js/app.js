window.app = {
    models: {},
    views: {},
    utils: {},

    loadingGoogleAPI: new $.Deferred(),
};

// Execute callbacks once Google API is loaded.
window.onloadGoogleAPI = function() {
    app.loadingGoogleAPI.resolve();
};

(function() {
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
}());
