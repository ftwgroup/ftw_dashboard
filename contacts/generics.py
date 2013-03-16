from django.views.generic.list import MultipleObjectMixin
from rest_framework import views, mixins, generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from contacts.serializers import ContactSerializer


# @api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'contacts': reverse('contact-list', request=request),
        })

class FTWAPIView(views.APIView):
    serializer_class = None
    # filter_backend = api_settings.FILTER_BACKEND
    def filter_queryset(self, queryset):
        """
        Filter our list from cassandra
        """
        return queryset

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, instance=None, data=None,
                       files=None, many=False, partial=False):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.serializer_class
        context = self.get_serializer_context()
        return serializer_class(instance, data=data, files=files,
                                many=many, partial=partial, context=context)

    def pre_save(self, obj):
        """
        Placeholder method for calling before saving an object.
        May be used eg. to set attributes on the object that are implicit
        in either the request, or the url.
        """
        pass

    def post_save(self, obj, created=False):
        """
        Placeholder method for calling after saving an object.
        """
        pass

class FTWMultiObjectMixin(MultipleObjectMixin):
    def get_queryset(self):
        # TODO change this to be a dynamic row key
        serializer = self.get_serializer()
        queryset = serializer.cf.get('FTW') # we may need to set this to retrieve more than 100 contacts
        return queryset

    def get_serializer(self, instance=None, data=None,
                       files=None, many=False, partial=False):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.serializer_class
        context = self.get_serializer_context()
        return serializer_class(instance, data=data, files=files,
                                many=many, partial=partial, context=context, cf=self.column_family)

class FTWListCreateView(generics.ListCreateAPIView, FTWMultiObjectMixin):
    """
    API endpoint that represents
    """
    serializer_class = ContactSerializer
