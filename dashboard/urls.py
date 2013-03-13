from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from dashboard.views import GoogleDriveListView, PitchListView, PitchDetailView

urlpatterns = patterns('dashboard.views',
    url(r'^$', 'login', name='dashboard_login'),
    url(r'^logout/$', 'logout', name='dashboard_logout'),
    url(r'^google_oauth2/$', 'google_oauth2_callback', name='dashboard_google_oauth2'),

    url(r'^main/$', 'main', name='dashboard_main'),

    # Google Drive views.
    url(r'^googledrive$', GoogleDriveListView.as_view(), name='googledrive_list'),

    # Pitch API views.  These use Backbone-compatible URLs (no trailing slash).
    url(r'^pitches$', PitchListView.as_view(), name='pitch_list'),
    url(r'^pitches/(?P<pk>\d+)$', PitchDetailView.as_view(), name='pitch_detail'),
    url(r'^pitches/(?P<pk>\d+)/import/$', 'import_googledrive_file', name='pitch_import'),
)
