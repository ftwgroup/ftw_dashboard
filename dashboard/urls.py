from django.conf.urls import patterns, url
from django.views.generic import TemplateView

import dashboard.views

urlpatterns = patterns('dashboard.views',
    url(r'^$', 'main', name='dashboard_main'),

    url(r'^google-auth-credentials/$', dashboard.views.GoogleAuthCredentials.as_view(), name='dashboard_google_auth_credentials'),
    url(r'^logout/$', 'logout', name='dashboard_logout'),

    # Pitch API views.  These use Backbone-compatible URLs (no trailing slash).
    url(r'^pitches$', dashboard.views.PitchListView.as_view(), name='pitch_list'),
    url(r'^pitches/(?P<pk>\d+)$', dashboard.views.PitchDetailView.as_view(), name='pitch_detail'),
    url(r'^pitches/(?P<pk>\d+)/import/$', 'import_googledrive_file', name='pitch_import'),
)

from django.conf import settings
def javascript_settings():
    return {
        'GOOGLE_OAUTH2_API_KEY': settings.GOOGLE_OAUTH2_API_KEY,
        'GOOGLE_OAUTH2_CLIENT_ID': settings.GOOGLE_OAUTH2_CLIENT_ID,
    }
