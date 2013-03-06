import json
import urllib, urllib2

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from oauth2client.client import OAuth2WebServerFlow
from rest_framework import generics

from dashboard.models import Pitch
from dashboard.serializers import PitchSerializer

google_oauth2_scope = " ".join(["https://www.googleapis.com/auth/%s" % s for s in ('userinfo.email', 'userinfo.profile', 'drive')])
google_oauth2_flow = OAuth2WebServerFlow(
    settings.GOOGLE_OAUTH2_CLIENT_ID,
    settings.GOOGLE_OAUTH2_CLIENT_SECRET,
    google_oauth2_scope,
    redirect_uri=settings.GOOGLE_OAUTH2_REDIRECT_URI,
)

def login(request, template="dashboard/login.html"):
    if request.method == 'GET':
        context = {
            'google_oauth2_url': google_oauth2_flow.step1_get_authorize_url()
        }
        return TemplateResponse(request, template, context)
    else:
        raise Http404

def google_oauth2_callback(request):
    error = request.GET.get('error')
    if error:
        # Show login error page.
        return TemplateResponse(request, "dashboard/login_error.html", {'error': error})
    else:
        # Use authorization code to request access token.
        code = request.GET.get('code')
        credentials = google_oauth2_flow.step2_exchange(code)
        GOOGLEAPIS_PROFILE = 'https://www.googleapis.com/oauth2/v1/userinfo'
        profile_data = {'access_token': credentials.access_token}
        profile_request = urllib2.Request(GOOGLEAPIS_PROFILE + '?' + urllib.urlencode(profile_data))
        profile_response = urllib2.urlopen(profile_request).read()
        profile = json.loads(profile_response)
        request.session['access_token'] = credentials.access_token
        request.session['token_expiry'] = credentials.token_expiry
        request.session['name'] = profile['name']
        request.session['email'] = profile['email']
        # Get user profile information.
        return redirect('dashboard_main')

def logout(request):
    request.session.clear()
    return redirect('dashboard_login')


def main(request, template="dashboard/main.html"):
    if not request.session.get('access_token'):
        return redirect('dashboard_login')

    context = {
        'access_token': request.session['access_token'],
        'name': request.session['name'],
        'email': request.session['email'],
    }
    return TemplateResponse(request, template, context)


class PitchListView(generics.ListCreateAPIView):
    model = Pitch
    serializer_class = PitchSerializer

class PitchDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = Pitch
    serializer_class = PitchSerializer
