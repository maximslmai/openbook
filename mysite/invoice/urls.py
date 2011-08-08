from django.conf.urls.defaults import *
from django.views.generic import list_detail
from mysite.invoice.models import Invoice

invoice_info = {
    'queryset': Invoice.objects.all(),
    'template_name': 'invoice_list.html',
}

urlpatterns = patterns('',
    (r'^invoice_list/$', list_detail.object_list, invoice_info)
)