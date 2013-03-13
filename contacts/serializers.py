from django.conf import settings
from pycassa import ColumnFamily, ConnectionPool
from rest_framework import serializers
from contacts.models import Contact

__author__ = 'michael'

POOL =  ConnectionPool(settings.CONTACT_KEYSPACE, settings.CASSANDRA_NODE_LIST)

class FTWSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        if kwargs.has_key('cf'):
            self.cf = ColumnFamily(POOL, kwargs['cf'])
        else:
            raise AttributeError("must specify a column family (cf)")
        del kwargs['cf']
        super(FTWSerializer, self).__init__(*args, **kwargs)


    def save(self):
        '''
        Persist this object to database
        '''
        if not hasattr(self.object, "row_key"):
            raise AttributeError("Object must have a row_key attr")

        self.cf.insert(self.object.row_key, self.object.return_dict())

        return self.object




class ContactSerializer(FTWSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    #created = serializers.DateTimeField()

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.email = attrs['email']
            instance.first_name = attrs['first_name']
            instance.last_name = attrs['last_name']
            #instance.created = attrs['created']
            return instance
        return Contact(**attrs)
