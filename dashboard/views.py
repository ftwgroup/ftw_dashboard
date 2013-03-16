from datetime import datetime
import httplib2
import json
import urllib, urllib2

import apiclient.discovery
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from oauth2client.client import OAuth2Credentials, OAuth2WebServerFlow
from rest_framework import generics as rest_generics
from rest_framework import status as rest_status
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.models import Pitch
from dashboard.serializers import PitchSerializer


def main(request, template="dashboard/main.html"):
    return TemplateResponse(request, template)


def logout(request):
    request.session.clear()
    return redirect('dashboard_login')


class GoogleAuthCredentials(APIView):
    def get(self, request, format=None):
        if 'credentials' in request.session:
            payload = request.session['credentials'].to_json()
            return Response(payload)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        access_token = request.DATA['access_token']
        expires_at = request.DATA['expires_at']
        refresh_token = request.DATA.get('refresh_token', None)
        id_token = request.DATA.get('id_token', None)
        token_expiry = datetime.fromtimestamp(int(expires_at))
        token_uri = "https://accounts.google.com/o/oauth2/token"
        user_agent = None
        request.session['credentials'] = OAuth2Credentials(
            access_token,
            settings.GOOGLE_OAUTH2_CLIENT_ID,
            settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            refresh_token,
            token_expiry,
            token_uri,
            user_agent,
            id_token=id_token,
        )
#        print "credentials = %s" % request.session['credentials'].to_json()
        return Response("OK")


class PitchListView(rest_generics.ListCreateAPIView):
    model = Pitch
    serializer_class = PitchSerializer

class PitchDetailView(rest_generics.RetrieveUpdateDestroyAPIView):
    model = Pitch
    serializer_class = PitchSerializer

def import_googledrive_file(request, pk=None):
    pitch = get_object_or_404(Pitch, pk=pk)
    docid = request.POST.get('docid')
    credentials = request.session['credentials']
    if not docid or not credentials:
        raise Http404

    http = credentials.authorize(httplib2.Http())
    drive = apiclient.discovery.build('drive', 'v2', http=http)
    document = drive.files().get(fileId=docid).execute()
    if "text/plain" in document.get('exportLinks', {}):
        url = document['exportLinks']["text/plain"]
        response, content = http.request(url)
        if response.status == 200:
            pitch.description = content
            pitch.save()
        return HttpResponse("OK")
    else:
        raise Http404
