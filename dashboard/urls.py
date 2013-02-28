from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from dashboard.views import PitchListView, PitchDetailView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="dashboard/main.html")),

    # Pitch API views.  These use Backbone-compatible URLs (no trailing slash).
    url(r'^pitches$', PitchListView.as_view(), name='pitch_list'),
    url(r'^pitches/(?P<pk>\d+)$', PitchDetailView.as_view(), name='pitch_detail'),
)
