from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^invoice/report/$', 'mysite.invoice.admin_views.report'),
    (r'^about/$', direct_to_template, {'template':'about.html'}),
    (r'^', include(admin.site.urls)),
)

urlpatterns += patterns('',
(r'^static/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/maxim/django_projects/media/'}),
)
