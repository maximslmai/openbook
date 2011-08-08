from django.db import models
from django.contrib import admin
from datetime import date as D


'''
Model design for the invoice application,

Invoice{
id: int; 
name: string;
date: date;
address: string; 
city: string;
shipping_date: date;
shipping_cost: int;
}
constrains & relations:
1. if a *shipping_date* is present, then *address* and *city* must present as well
2. *id* and *date* are required at all time
======================

Item{
id: int;
name: string;
invoice_id: int; Invoice.id;
price: int;
quantity: int;
}

constrains & relations:
1. all the attributes are required in this model
2. *invoice_id* is the foreign reference to *id*  in the Invoice model.
=======================

Invoice one-to-more Item

'''
# Create your models here.
class Invoice(models.Model):
    CITY_CHOICES = (
    (u'Ajax ', u'Ajax '),
    (u'Ancaster ', u'Ancaster '),
    (u'Balm Beach ', u'Balm Beach '),
    (u'Barrie ', u'Barrie '),
    (u'Beeton ', u'Beeton '),
    (u'Bowmanville ', u'Bowmanville '),
    (u'Brampton ', u'Brampton '),
    (u'Burlington ', u'Burlington '),
    (u'Cambridge ', u'Cambridge '),
    (u'Cobourg ', u'Cobourg '),
    (u'Downsview ', u'Downsview '),
    (u'Georgetown ', u'Georgetown '),
    (u'Glen Williams ', u'Glen Williams '),
    (u'Guelph ', u'Guelph '),
    (u'Hamilton ', u'Hamilton '),
    (u'Kincardine ', u'Kincardine '),
    (u'King City ', u'King City '),
    (u'Kitchener ', u'Kitchener '),
    (u'Lindsay ', u'Lindsay '),
    (u'Markham ', u'Markham '),
    (u'Midland ', u'Midland '),
    (u'Milton ', u'Milton '),
    (u'Mississauga ', u'Mississauga '),
    (u'Mount Forest ', u'Mount Forest '),
    (u'New Hamburg ', u'New Hamburg '),
    (u'Newmarket ', u'Newmarket '),
    (u'North York ', u'North York '),
    (u'Oakville ', u'Oakville '),
    (u'Omemee ', u'Omemee '),
    (u'Oshawa ', u'Oshawa '),
    (u'Peterborough ', u'Peterborough '),
    (u'Pickering ', u'Pickering '),
    (u'Point Clark ', u'Point Clark '),
    (u'Rexdale ', u'Rexdale '),
    (u'Richmond Hill ', u'Richmond Hill '),
    (u'Scarborough ', u'Scarborough '),
    (u'Stoney Creek ', u'Stoney Creek '),
    (u'Toronto ', u'Toronto '),
    (u'Trenton ', u'Trenton '),
    (u'Vaughan ', u'Vaughan '),
    (u'Waterloo ', u'Waterloo '),
    (u'Whitby ', u'Whitby '),
    (u'Yorkville', u'Yorkville'),
    )
    
    name = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    date.default = str(D.today())
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, choices=CITY_CHOICES, blank=True)
    phone1 = models.CharField(max_length=10, blank=True)
    phone2 = models.CharField(max_length=10, blank=True)
    total = models.IntegerField()
    total.default = 0
    delivery = models.BooleanField()
    shipping_pickup_date = models.DateField()
    shipping_pickup_date.default = str(D.today())
    shipping_handling = models.IntegerField()
    shipping_handling.default = 0
        
    def __str__(self):
        return u'%s - %s, %s - %s, Total: $%d ' % (self.name, self.address, self.city, self.date, self.total)

    def __unicode__(self):
        return u'%s - %s, %s - %s, %s ' % (self.name, self.address, self.city, self.date, self.subtotal())
    

    def tax(self):
        tax = round((self.total / 1.13)*0.13, 2)
        return "$"+str(tax)
    tax.short_description = 'Tax'

    def subtotal(self):
        subtotal = round(self.total / 1.13, 2)
        return "$"+str(subtotal)
    subtotal.short_description = 'Subtotal' 
 
    def save(self):
        if self.id is not None:
            old_invoice = Invoice.objects.get(pk=self.id)
            self.total = self.total - old_invoice.shipping_handling + self.shipping_handling
            super(Invoice, self).save()
        else:
            self.total = self.shipping_handling
            super(Invoice, self).save()
        
    def delete(self):
        items = Item.objects.filter(invoice=self)
        for item in items:
            item.delete()
        super(Invoice, self).delete()
        
    def get_absolute_url(self):
        return "/invoice/invoice/%i/" % self.id
    
class Item(models.Model):
    
    invoice = models.ForeignKey(Invoice)
    quantity = models.IntegerField()
    price = models.IntegerField()
    name = models.CharField(max_length=128)
    
    def save(self, **kwargs):

        # edit existing
        if self.id is not None:
            old_item = Item.objects.get(pk=self.id)
            old_total = old_item.price * old_item.quantity
            super(Item, self).save()
            self.invoice.total = self.invoice.total - old_total + (self.price * self.quantity)
            self.invoice.save()
        # add new
        else:
            super(Item, self).save()
            self.invoice.total = self.invoice.total + (self.price * self.quantity)
            self.invoice.save()
    
    def delete(self):
        super(Item, self).delete()
        self.invoice.total = self.invoice.total - (self.price * self.quantity)
        self.invoice.save()
        
    def __str__(self):
        return u'%s - $%d @ %s' % (self.name, self.price, self.quantity)
    
    def __unicode__(self):
        return u'%s - $%d @ %s' % (self.name, self.price, self.quantity)

