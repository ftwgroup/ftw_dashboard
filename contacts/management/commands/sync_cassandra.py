from pycassa.system_manager import *
from django.conf import settings
from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from pycassa.types import CompositeType


class Command(BaseCommand):

    def handle(self, *args, **options):
        sys = SystemManager()#(settings.CASSANDRA_HOST)

        # If there is already a Contact keyspace, we have to ask the user
        # what they want to do with it.
        print sys.list_keyspaces()
        if settings.CONTACT_KEYSPACE in sys.list_keyspaces():
            msg = 'Looks like you already have a ' + settings.CONTACT_KEYSPACE + ' keyspace.\nDo you '
            msg += 'want to delete it and recreate it? All current data will '
            msg += 'be deleted! (y/n): '
            resp = raw_input(msg)
            if not resp or resp[0] != 'y':
                print "Ok, then we're done here."
                return
            sys.drop_keyspace(settings.CONTACT_KEYSPACE)

        sys.create_keyspace(settings.CONTACT_KEYSPACE, SIMPLE_STRATEGY, {'replication_factor': '1'})

        comparator1 = CompositeType(UTF8_TYPE, UTF8_TYPE)
        sys.create_column_family(settings.CONTACT_KEYSPACE, 'Contacts', comparator_type=UTF8_TYPE)
        sys.create_column_family(settings.CONTACT_KEYSPACE, 'ContactsList', comparator_type=comparator1)
        # comparator2 = CompositeType(TIME_UUID_TYPE, DATE_TYPE)
        sys.create_column_family(settings.CONTACT_KEYSPACE, 'Emails', comparator_type=UTF8_TYPE)

        print 'All done!'

