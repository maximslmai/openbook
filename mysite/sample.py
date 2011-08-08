from invoice.models import Invoice, Item
import datetime
from random import randint


names = !cat /home/maxim/random_names
streets = !cat /home/maxim/random_streets
items = !cat /home/maxim/random_items

for i in range(300):
    name = names[randint(0, len(names)-2)]
    street_number = randint(1,2000)
    street_name = streets[randint(0,len(streets)-2)]
    d = datetime.date(randint(2006,2010), randint(1,12), randint(1,27))
    shipping_pickup_date = datetime.date(randint(2000,2010), randint(1,12), randint(1,27))
    address = str(street_number) + " " + street_name
    city = "Toronto"
    shipping_handling = randint(10,50)
    invoice = Invoice(name=name, date=d, address=address, city=city, shipping_pickup_date=shipping_pickup_date, shipping_handling=shipping_handling)
    invoice.save()
    for i in range(randint(5,12)):
        item_name = items[randint(0, len(items)-2)]
        price = randint(50,300)
        quantity = randint(1,5)
        item = Item(name=item_name, invoice=invoice, price=price, quantity=quantity)
        item.save()
        print name + " - " + address + ": " + item_name + " = " + str(price) + " * " + str(quantity)


for i in range(100):
    name = names[randint(0, len(names)-2)]
    street_number = randint(1,2000)
    street_name = streets[randint(0,len(streets)-2)]
    d = datetime.date(2011, 1, randint(1,22))
    shipping_pickup_date =datetime.date(2011, 1, randint(1,22))
    address = str(street_number) + " " + street_name
    city = "Toronto"
    shipping_handling = randint(10,50)
    invoice = Invoice(name=name, date=d, address=address, city=city, shipping_pickup_date=shipping_pickup_date, shipping_handling=shipping_handling)
    invoice.save()
    for i in range(randint(5,12)):
        item_name = items[randint(0, len(items)-2)]
        price = randint(50,300)
        quantity = randint(1,5)
        item = Item(name=item_name, invoice=invoice, price=price, quantity=quantity)
        item.save()
        print name + " - " + address + ": " + item_name + " = " + str(price) + " * " + str(quantity)
