import datetime
from django.db import models
from pycassa import ConnectionPool, ColumnFamily
import uuid
from ftw_cassandra.cassandra import Cassandra
from ftw_dashboard import settings

# POOL = ConnectionPool(settings.CONTACT_KEYSPACE, settings.CASSANDRA_NODE_LIST)
# CF_CONTACTS = ColumnFamily(POOL, 'Contacts')
# CF_CONTACTS_LIST = ColumnFamily(POOL, 'ContactsList')
# CF_EMAILS = ColumnFamily(POOL, 'Emails')

def create_contact_list(contacts_dict):
    new_contacts = {}
    for key, value in contacts_dict.iteritems():
        if new_contacts.has_key(key[0]):
            setattr(new_contacts[key[0]], key[1], value)
        else:
            new_contacts[key[0]] = Contact(**{key[1]: value,
                                              'uid': key[0]})
    return new_contacts.values()

class Contact(object):

    def __init__(self, email=None, first_name=None, last_name=None, created=None, uid = None, row_key=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        #self.created = created or datetime.datetime.now()

        # TODO: pull the firm identified from a rdbms and will prefix all row_keys
        self.row_key = row_key
        if not row_key:
            self.row_key = 'FTW'

        self.uid = uid
        if not uid:
            self.uid = uuid.uuid1().hex


    def return_dict(self):
        return {
            'uid': self.uid,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            #'created': self.created
            }

version = '0.1'