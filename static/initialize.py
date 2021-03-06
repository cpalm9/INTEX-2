from datetime import datetime
import os
# initialize the django environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'fomo.settings'
import django
django.setup()
from catalog import models as cmod
from account import models as amod
from decimal import Decimal
from django.core import management
from django.db import connection
from datetime import datetime
import os, os.path, sys

# ensure the user really wants to do this
areyousure = input('''
  You are about to drop and recreate the entire database.
  All data are about to be deleted.  Use of this script
  may cause itching, vertigo, dizziness, tingling in
  extremities, loss of balance or coordination, slurred
  speech, temporary zoobie syndrome, longer lines at the
  testing center, changed passwords in Learning Suite, or
  uncertainty about whether to call your professor
  'Brother' or 'Doctor'.
  Please type 'yes' to confirm the data destruction: ''')
if areyousure.lower() != 'yes':
    print()
    print('  Wise choice.')
    sys.exit(1)

# drop and recreate the database tables
print()
print('Living on the edge!  Dropping the current database tables.')
with connection.cursor() as cursor:
    cursor.execute("DROP SCHEMA public CASCADE")
    cursor.execute("CREATE SCHEMA public")
    cursor.execute("GRANT ALL ON SCHEMA public TO postgres")
    cursor.execute("GRANT ALL ON SCHEMA public TO public")

# make the migrations and migrate
management.call_command('makemigrations', 'account', 'catalog')
management.call_command('migrate')

# imports for our project
from account.models import FomoUser
from django.contrib.auth.models import Permission, Group

#Create Groups
g1 = Group()
g1.name = 'Admin'
g1.save()

for p in Permission.objects.all():
    g1.permissions.add(p)


g2 = Group()
g2.name = 'Manager'
g2.save()

g2.permissions.add(Permission.objects.get(codename= 'add_logentry'))
g2.permissions.add(Permission.objects.get(codename= 'change_fomouser'))
g2.permissions.add(Permission.objects.get(codename= 'delete_logentry'))
g2.permissions.add(Permission.objects.get(codename= 'change_logentry'))

#create custom permissions
# content_type = ContentType.objects.get_for_model(FomoUser)
# permission = Permission.objects.create(
#     codename = 'add_product',
#     name = 'Add a new product to our system',
#     content_type = content_type,
# )
# g1.permissions.add(permission)

#User Objects
u1 = amod.FomoUser()
u1.username = 'u1'
u1.first_name = 'Sean'
u1.last_name = 'Burnham'
u1.email = 'sburnham92@gmail.com'
u1.birth_date = datetime(1992, 10, 13)
u1.phone = '209-402-1604'
u1.address = '123 Happy St.'
u1.city = 'Provo'
u1.state = 'UT'
u1.zipcode = '84606'
u1.set_password('password')
u1.is_staff=True
u1.is_admin = True
u1.is_superuser = True
u1.save()

u1.groups.add(g1)

# p = Permission.objects.get()
# u1.user_permissions.add(p)
# for p in Permission.objects.all():
#     u1.user_permissions.add(p)


u2 = amod.FomoUser()
u2.username = 'u2'
u2.first_name = 'Spencer'
u2.last_name = 'Finnegan'
u2.email = 'spencerfinnegan@gmail.com'
u2.birth_date = datetime(1992, 10, 13)
u2.phone = '636-688-9225'
u2.address = '615 N 100 W'
u2.city = 'Provo'
u2.state = 'UT'
u2.zipcode = '84601'
u2.set_password('password')
u2.is_staff=True
u2.save()

u2.groups.add(g2)

u3 = amod.FomoUser()
u3.username = 'u3'
u3.first_name = 'Zac'
u3.last_name = 'Clark'
u3.email = 'test@test.com'
u3.birth_date = datetime(1992, 10, 13)
u3.phone = '555-555-5555'
u3.address = '123 ABC St.'
u3.city = 'provo'
u3.state = 'UT'
u3.zipcode = '12345'
u3.set_password('password3')
u3.is_staff=True
u3.save()

u3.groups.add(g2)

u4 = amod.FomoUser()
u4.username = 'u4'
u4.first_name = "Chris"
u4.last_name = "Palmer"
u4.email = "chris.palmer19@outlook.com"
u4.birth_date = datetime(1992, 10, 13)
u4.phone = "801 372 2699"
u4.address = "148 E 1460 S"
u4.city = 'Provo'
u4.state = "UT"
u4.zipcode = "84058"
u4.set_password('password4')
u4.is_staff=True
u4.save()

u4.groups.add(g2)
# multiple queries

# u1 = amod.objects.get(id = 1)
# print(u1.id, u1.first_name)
#
# users = amod.objects.filter(city = 'Provo')
# for u1 in users:
#     print(u1.id, u1.city)
#
# users = amod.objects.all()
# for u1 in users:
#     print(u1.id, u1.state)
#
# users = amod.objects.filter(id__lt = 6)
# for u1 in users:
#     print(u1.id, u1.city)

#Categories
cat1 = cmod.Category()
cat1.code = 'brass'
cat1.name = 'Brass Instruments'
cat1.save()

cat2 = cmod.Category()
cat2.code = 'woodwind'
cat2.name = 'Woodwind Instruments'
cat2.save()

cat3 = cmod.Category()
cat3.code = 'strings'
cat3.name = 'String Instruments'
cat3.save()

cat4 = cmod.Category()
cat4.code = 'plastic'
cat4.name = 'Plastic Instruments'
cat4.save()

cat5 = cmod.Category()
cat5.code = 'percussion'
cat5.name = 'Percussion Instruments'
cat5.save()

#Create Products
bp1 = cmod.BulkProduct()
bp1.category = cat4
bp1.name = 'Kazoo'
bp1.brand = 'ToysRUs'
bp1.price = Decimal('.50')
bp1.quantity = 20
bp1.reorder_trigger = 5
bp1.reorder_qty = 15
bp1.save()

bp2 = cmod.BulkProduct()
bp2.category = cat2
bp2.name = 'Harmonica'
bp2.brand = 'Hohner'
bp2.price = Decimal('4.50')
bp2.quantity = 15
bp2.reorder_trigger = 5
bp2.reorder_qty = 10
bp2.save()

bp3 = cmod.BulkProduct()
bp3.category = cat2
bp3.name = 'Recorder'
bp3.brand = 'ToysRUs'
bp3.price = Decimal('2.50')
bp3.quantity = 10
bp3.reorder_trigger = 5
bp3.reorder_qty = 5
bp3.save()

up1 = cmod.UniqueProduct()
up1.category = cat1
up1.name = 'Trumpet'
up1.brand = 'Yamaha'
up1.price = Decimal('449.99')
up1.serial_number = 'xyz1'
up1.save()

up2 = cmod.UniqueProduct()
up2.category = cat2
up2.name = 'Saxophone'
up2.brand = 'Accent'
up2.price = Decimal('514.50')
up2.serial_number = 'xyz2'
up2.save()

up3 = cmod.UniqueProduct()
up3.category = cat2
up3.name = 'Guitar'
up3.brand = 'Rogue'
up3.price = Decimal('702.50')
up3.serial_number = 'xyz3'
up3.save()

rp1 = cmod.RentalProduct()
rp1.category = cat1
rp1.name = 'Trumpet'
rp1.brand = 'Yamaha'
rp1.quantity = 3
rp1.price = Decimal('25')
rp1.serial_number = 'zyx1'
rp1.save()

rp2 = cmod.RentalProduct()
rp2.category = cat2
rp2.name = 'Flute'
rp2.brand = 'Yamaha'
rp2.quantity = 7
rp2.price = Decimal('18')
rp2.serial_number = 'zyx2'
rp2.save()

rp3 = cmod.RentalProduct()
rp3.category = cat5
rp3.name = 'Snare Drum'
rp3.brand = 'Yamaha'
rp3.quantity = 4
rp3.price = Decimal('32')
rp3.serial_number = 'zyx3'
rp3.save()

