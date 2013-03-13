from contacts.generics import FTWListCreateView
from contacts.serializers import ContactSerializer


class ContactsListCreateView(FTWListCreateView):
    serializer_class = ContactSerializer
    column_family = 'ContactsList'