from rest_framework import generics

from dashboard.models import Pitch
from dashboard.serializers import PitchSerializer

class PitchListView(generics.ListCreateAPIView):
    model = Pitch
    serializer_class = PitchSerializer

class PitchDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = Pitch
    serializer_class = PitchSerializer
