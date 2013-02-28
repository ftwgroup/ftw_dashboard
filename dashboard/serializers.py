from rest_framework import serializers

from dashboard.models import Pitch

class PitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitch
        fields = ('id', 'snippet', 'description', 'image')
