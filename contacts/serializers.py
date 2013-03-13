from django.conf import settings
from pycassa import ColumnFamily, ConnectionPool
from rest_framework import serializers
from contacts.models import Contact

POOL =  ConnectionPool(settings.CONTACT_KEYSPACE, settings.CASSANDRA_NODE_LIST)

class FTWSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        if kwargs.has_key('cf'):
            self.cf = ColumnFamily(POOL, kwargs['cf'])
        else:
            raise AttributeError("must specify a column family (cf)")
        del kwargs['cf']
        super(FTWSerializer, self).__init__(*args, **kwargs)

    def get_cassandra_columns(self):
        raise NotImplementedError("please implement this and have it return the appropriate dict")
    def save(self):
        '''
        Persist this object to database
        '''
        if not hasattr(self.object, "row_key"):
            raise AttributeError("Object must have a row_key attr")
        if not hasattr(self.object, 'uid'):
            raise AttributeError("Object must have a uuid attr")

        self.cf.insert(self.object.row_key, self.get_cassandra_columns())

        return self.object

class ContactSerializer(FTWSerializer):
    uid = serializers.CharField(max_length=200, required=False)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    #created = serializers.DateTimeField()

    def get_cassandra_columns(self):
        contact_dict = {(self.object.uid, 'email'): self.object.email,
                        (self.object.uid, 'first_name'): self.object.first_name,
                        (self.object.uid, 'last_name'): self.object.last_name}

        return contact_dict

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.uid = attrs['uid']
            instance.email = attrs['email']
            instance.first_name = attrs['first_name']
            instance.last_name = attrs['last_name']
            #instance.created = attrs['created']
            return instance
        return Contact(**attrs)
