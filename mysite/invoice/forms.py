from django.forms import ModelForm, CharField, ValidationError
from invoice.models import Invoice, Item

class InvoiceForm(ModelForm):
    def __init__(self, data=None, *args, **kwargs):
        if data=={}:
            data=None
        ModelForm.__init__(self, data, *args, **kwargs)
    class Meta:
        model=Invoice
        
class ItemForm(ModelForm):
    def __init__(self, data=None, *args, **kwargs):
        if data=={}:
            data=None
        ModelForm.__init__(self, data, *args, **kwargs)
    class Meta:
        model=Item