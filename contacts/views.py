from contacts.generics import FTWListCreateView
from contacts.models import create_contact_list
from contacts.serializers import ContactSerializer


class ContactsListCreateView(FTWListCreateView):
    serializer_class = ContactSerializer
    column_family = 'ContactsList'

    def get_queryset(self):
        # TODO change this to be a dynamic row key
        serializer = self.get_serializer()
        contacts_dict = serializer.cf.get('FTW')  # we may need to set this to retrieve more than 100 contacts
        queryset = create_contact_list(contacts_dict)
        return queryset
