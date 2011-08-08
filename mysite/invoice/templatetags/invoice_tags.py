from django import template
from invoice.models import Invoice, Item
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


register = template.Library()

@login_required
@register.inclusion_tag("invoice/invoice_tags.html")
def sidepanel():
    # for invoices_to_ship module
    invoices = Invoice.objects.filter(shipping_date = date.today())
    
    # for view_invoices_in_month module
    dates = []
    all_invoices = Invoice.objects.order_by("-date")[:16]
    for i in all_invoices:
        year_month = str(i.date.year)+"/" + str(i.date.month)
        if not year_month in dates:
            dates.append(year_month)
     
    return {"invoices":invoices, "year_month": dates}
