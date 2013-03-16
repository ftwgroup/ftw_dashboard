from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from contacts.views import ContactsListCreateView


urlpatterns = patterns('',
    # Examples:
    url(r'^$', ContactsListCreateView.as_view(), name='contact-list'),

# Uncomment the admin/doc line below to enable admin documentation:
# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

# Uncomment the next line to enable the admin:
# url(r'^admin/', include(admin.site.urls)),
)
