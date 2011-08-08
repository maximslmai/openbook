import sys

sys.path.append("/home/maxim/django_projects/mysite/")

from invoice.models import Invoice, Item
from django.contrib import admin
from django.shortcuts import redirect

class ItemInline(admin.TabularInline):
    model = Item
    extra = 0

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'address', 'city', 'phone1' ,'phone2', 'shipping_pickup_date', 'delivery', 'shipping_handling', 'subtotal','tax', 'total',)
    list_filter = ('date', 'shipping_pickup_date',)
    readonly_fields = ('total',)
    ordering = ('-date',)
    search_fields = ('name', 'address', 'phone1', 'phone2',)
    date_hierarchy = 'date'
    inlines = [ItemInline]
    
    def change_view(self, request, object_id, extra_context=None):
        if request.user.is_superuser:
            self.readonly_fields = ()
        else:
            self.exclude = ('total',)
        return super(InvoiceAdmin, self).change_view(request, object_id,
            extra_context=None)

admin.site.register(Invoice,InvoiceAdmin)
