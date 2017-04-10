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
u1.save()

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
cat4.code = 'accessory'
cat4.name = 'Accessories'
cat4.save()

cat5 = cmod.Category()
cat5.code = 'percussion'
cat5.name = 'Percussion Instruments'
cat5.save()

#Create Products
bp1 = cmod.BulkProduct()
bp1.category = cat4
bp1.name = 'Bassoon Reed'
bp1.brand = 'change this'
bp1.price = Decimal('.50')
bp1.quantity = 20
bp1.reorder_trigger = 5
bp1.reorder_qty = 15
bp1.path = '/static/homepage/media/images/instruments/accessories/bassoon_reed.png/'
bp1.save()

pp1 = cmod.ProductPicture()
pp1.product = bp1
pp1.path = '/static/homepage/media/images/instruments/accessories/bassoon_reed.png/'
pp1.save()

bp2 = cmod.BulkProduct()
bp2.category = cat4
bp2.name = 'Drum Sticks'
bp2.brand = 'wood'
bp2.price = Decimal('4.50')
bp2.quantity = 15
bp2.reorder_trigger = 5
bp2.reorder_qty = 10
bp2.path = '/static/homepage/media/images/instruments/accessories/drum_sticks.png/'
bp2.save()

pp2 = cmod.ProductPicture()
pp2.product = bp2
pp2.path = '/static/homepage/media/images/instruments/accessories/drum_sticks.png/'
pp2.save()

bp3 = cmod.BulkProduct()
bp3.category = cat4
bp3.name = 'Electric Guitar String'
bp3.brand = 'ToysRUs'
bp3.price = Decimal('2.50')
bp3.quantity = 10
bp3.reorder_trigger = 5
bp3.reorder_qty = 5
bp3.path = '/static/homepage/media/images/instruments/accessories/electric_guitar_strings1.png/'
bp3.save()

pp3 = cmod.ProductPicture()
pp3.product = bp3
pp3.path = '/static/homepage/media/images/instruments/accessories/electric_guitar_strings1.png/'
pp3.save()

pp4 = cmod.ProductPicture()
pp4.product = bp3
pp4.path = '/static/homepage/media/images/instruments/accessories/electric_guitar_string2.png/'
pp4.save()

bp4 = cmod.BulkProduct()
bp4.category = cat4
bp4.name = 'Guitar Amp'
bp4.brand = 'ToysRUs'
bp4.price = Decimal('2.50')
bp4.quantity = 10
bp4.reorder_trigger = 5
bp4.reorder_qty = 5
bp4.path = '/static/homepage/media/images/instruments/accessories/guitar_amp.png/'
bp4.save()

pp5 = cmod.ProductPicture()
pp5.product = bp4
pp5.path = '/static/homepage/media/images/instruments/accessories/guitar_amp.png/'
pp5.save()

bp5 = cmod.BulkProduct()
bp5.category = cat4
bp5.name = 'Guitar Picks'
bp5.brand = 'ToysRUs'
bp5.price = Decimal('2.50')
bp5.quantity = 10
bp5.reorder_trigger = 5
bp5.reorder_qty = 5
bp5.path = '/static/homepage/media/images/instruments/accessories/guitar_picks.png/'
bp5.save()

pp6 = cmod.ProductPicture()
pp6.product = bp5
pp6.path = '/static/homepage/media/images/instruments/accessories/guitar_picks.png/'
pp6.save()

pp7 = cmod.ProductPicture()
pp7.product = bp5
pp7.path = '/static/homepage/media/images/instruments/accessories/guitar_picks_1.png/'
pp7.save()

pp8 = cmod.ProductPicture()
pp8.product = bp5
pp8.path = '/static/homepage/media/images/instruments/accessories/guitar_picks_2.png/'
pp8.save()

bp6 = cmod.BulkProduct()
bp6.category = cat4
bp6.name = 'Guitar Strap'
bp6.brand = 'ToysRUs'
bp6.price = Decimal('2.50')
bp6.quantity = 10
bp6.reorder_trigger = 5
bp6.reorder_qty = 5
bp6.path = '/static/homepage/media/images/instruments/accessories/guitar_strap1.png/'
bp6.save()

pp9 = cmod.ProductPicture()
pp9.product = bp6
pp9.path = '/static/homepage/media/images/instruments/accessories/guitar_strap1.png/'
pp9.save()

pp10 = cmod.ProductPicture()
pp10.product = bp6
pp10.path = '/static/homepage/media/images/instruments/accessories/guitar_strap2.png/'
pp10.save()

pp11 = cmod.ProductPicture()
pp11.product = bp6
pp11.path = '/static/homepage/media/images/instruments/accessories/guitar_strap3.png/'
pp11.save()

bp7 = cmod.BulkProduct()
bp7.category = cat4
bp7.name = 'Guitar Strings'
bp7.brand = 'ToysRUs'
bp7.price = Decimal('2.50')
bp7.quantity = 10
bp7.reorder_trigger = 5
bp7.reorder_qty = 5
bp7.path = '/static/homepage/media/images/instruments/accessories/guitar_strings1.png/'
bp7.save()

pp12 = cmod.ProductPicture()
pp12.product = bp7
pp12.path = '/static/homepage/media/images/instruments/accessories/guitar_strings1.png/'
pp12.save()

pp13 = cmod.ProductPicture()
pp13.product = bp7
pp13.path = '/static/homepage/media/images/instruments/accessories/guitar_strings2.png/'
pp13.save()

bp8 = cmod.BulkProduct()
bp8.category = cat4
bp8.name = 'Guitar Tuner'
bp8.brand = 'ToysRUs'
bp8.price = Decimal('2.50')
bp8.quantity = 10
bp8.reorder_trigger = 5
bp8.reorder_qty = 5
bp8.path = '/static/homepage/media/images/instruments/accessories/guitar_tuner.png/'
bp8.save()

pp14 = cmod.ProductPicture()
pp14.product = bp8
pp14.path = '/static/homepage/media/images/instruments/accessories/guitar_tuner.png/'
pp14.save()

pp15 = cmod.ProductPicture()
pp15.product = bp8
pp15.path = '/static/homepage/media/images/instruments/accessories/guitar_tuner_2.png/'
pp15.save()

bp9 = cmod.BulkProduct()
bp9.category = cat4
bp9.name = 'Music Stand'
bp9.brand = 'ToysRUs'
bp9.price = Decimal('2.50')
bp9.quantity = 10
bp9.reorder_trigger = 5
bp9.reorder_qty = 5
bp9.path = '/static/homepage/media/images/instruments/accessories/music_stand.png/'
bp9.save()

pp16 = cmod.ProductPicture()
pp16.product = bp9
pp16.path = '/static/homepage/media/images/instruments/accessories/music_stand.png/'
pp16.save()

pp17 = cmod.ProductPicture()
pp17.product = bp9
pp17.path = '/static/homepage/media/images/instruments/accessories/music_stand_2.png/'
pp17.save()

pp18 = cmod.ProductPicture()
pp18.product = bp9
pp18.path = '/static/homepage/media/images/instruments/accessories/music_stand_3.png/'
pp18.save()

bp10 = cmod.BulkProduct()
bp10.category = cat4
bp10.name = 'Oboe Reed'
bp10.brand = 'ToysRUs'
bp10.price = Decimal('2.50')
bp10.quantity = 10
bp10.reorder_trigger = 5
bp10.reorder_qty = 5
bp10.path = '/static/homepage/media/images/instruments/accessories/oboe_reed.png/'
bp10.save()

pp19 = cmod.ProductPicture()
pp19.product = bp10
pp19.path = '/static/homepage/media/images/instruments/accessories/oboe_reed.png/'
pp19.save()

bp11 = cmod.BulkProduct()
bp11.category = cat4
bp11.name = 'Saxophone Mouthpiece'
bp11.brand = 'ToysRUs'
bp11.price = Decimal('2.50')
bp11.quantity = 10
bp11.reorder_trigger = 5
bp11.reorder_qty = 5
bp11.path = '/static/homepage/media/images/instruments/accessories/saxophone_mouthpiece.png/'
bp11.save()

pp20 = cmod.ProductPicture()
pp20.product = bp11
pp20.path = '/static/homepage/media/images/instruments/accessories/saxophone_mouthpiece.png/'
pp20.save()

bp12 = cmod.BulkProduct()
bp12.category = cat4
bp12.name = 'Saxophone Reeds'
bp12.brand = 'ToysRUs'
bp12.price = Decimal('2.50')
bp12.quantity = 10
bp12.reorder_trigger = 5
bp12.reorder_qty = 5
bp12.path = '/static/homepage/media/images/instruments/accessories/saxophone_reeds.png/'
bp12.save()

pp21 = cmod.ProductPicture()
pp21.product = bp12
pp21.path = '/static/homepage/media/images/instruments/accessories/saxophone_reeds.png/'
pp21.save()

bp13 = cmod.BulkProduct()
bp13.category = cat4
bp13.name = 'Sheet Music'
bp13.brand = 'ToysRUs'
bp13.price = Decimal('2.50')
bp13.quantity = 10
bp13.reorder_trigger = 5
bp13.reorder_qty = 5
bp13.path = '/static/homepage/media/images/instruments/accessories/sheet_music_1.png/'
bp13.save()

pp22 = cmod.ProductPicture()
pp22.product = bp13
pp22.path = '/static/homepage/media/images/instruments/accessories/sheet_music_1.png/'
pp22.save()

pp23 = cmod.ProductPicture()
pp23.product = bp13
pp23.path = '/static/homepage/media/images/instruments/accessories/sheet_music_2.png/'
pp23.save()

pp24 = cmod.ProductPicture()
pp24.product = bp13
pp24.path = '/static/homepage/media/images/instruments/accessories/sheet_music_3.png'
pp24.save()

bp14 = cmod.BulkProduct()
bp14.category = cat4
bp14.name = 'Trumpet Mouthpiece'
bp14.brand = 'ToysRUs'
bp14.price = Decimal('2.50')
bp14.quantity = 10
bp14.reorder_trigger = 5
bp14.reorder_qty = 5
bp14.path = '/static/homepage/media/images/instruments/accessories/trumpet_mouthpiece.png'
bp14.save()

pp25 = cmod.ProductPicture()
pp25.product = bp14
pp25.path = '/static/homepage/media/images/instruments/accessories/trumpet_mouthpiece.png'
pp25.save()

bp15 = cmod.BulkProduct()
bp15.category = cat4
bp15.name = 'Trumpet Mute'
bp15.brand = 'ToysRUs'
bp15.price = Decimal('2.50')
bp15.quantity = 10
bp15.reorder_trigger = 5
bp15.reorder_qty = 5
bp15.path = '/static/homepage/media/images/instruments/accessories/trumpet_mute1.png/'
bp15.save()

pp26 = cmod.ProductPicture()
pp26.product = bp15
pp26.path = '/static/homepage/media/images/instruments/accessories/trumpet_mute1.png/'
pp26.save()

pp27 = cmod.ProductPicture()
pp27.product = bp15
pp27.path = '/static/homepage/media/images/instruments/accessories/trumpet_mute2.png/'
pp27.save()

######################## Unique Products ##########################################
up1 = cmod.UniqueProduct()
up1.category = cat1
up1.name = 'French Horn'
up1.brand = 'Yamaha'
up1.price = Decimal('449.99')
up1.serial_number = 'xyz1'
up1.path = '/static/homepage/media/images/instruments/brass/double_1.png/'
up1.save()

pp28 = cmod.ProductPicture()
pp28.product = up1
pp28.path = '/static/homepage/media/images/instruments/brass/double_1.png/'
pp28.save()

pp29 = cmod.ProductPicture()
pp29.product = up1
pp29.path = '/static/homepage/media/images/instruments/brass/double_2.png/'
pp29.save()

up2 = cmod.UniqueProduct()
up2.category = cat1
up2.name = 'Fluglehorn'
up2.brand = 'Accent'
up2.price = Decimal('514.50')
up2.serial_number = 'xyz2'
up2.path = '/static/homepage/media/images/instruments/brass/flugelhorn_1.png/'
up2.save()

pp30 = cmod.ProductPicture()
pp30.product = up2
pp30.path = '/static/homepage/media/images/instruments/brass/flugelhorn_1.png/'
pp30.save()

pp31 = cmod.ProductPicture()
pp31.product = up2
pp31.path = '/static/homepage/media/images/instruments/brass/flugelhron_2.png/'
pp31.save()

pp32 = cmod.ProductPicture()
pp32.product = up2
pp32.path = '/static/homepage/media/images/instruments/brass/flugelhron_3.png/'
pp32.save()

up3 = cmod.UniqueProduct()
up3.category = cat1
up3.name = 'Trombone'
up3.brand = 'Accent'
up3.price = Decimal('514.50')
up3.serial_number = 'xyz2'
up3.path = '/static/homepage/media/images/instruments/brass/trombone_1.png/'
up3.save()

pp33 = cmod.ProductPicture()
pp33.product = up3
pp33.path = '/static/homepage/media/images/instruments/brass/trombone_1.png/'
pp33.save()

pp34 = cmod.ProductPicture()
pp34.product = up3
pp34.path = '/static/homepage/media/images/instruments/brass/trombone_2.png/'
pp34.save()

pp35 = cmod.ProductPicture()
pp35.product = up3
pp35.path = '/static/homepage/media/images/instruments/brass/trombone_3.png/'
pp35.save()

up4 = cmod.UniqueProduct()
up4.category = cat1
up4.name = 'Trumpet'
up4.brand = 'Accent'
up4.price = Decimal('514.50')
up4.serial_number = 'xyz2'
up4.path = '/static/homepage/media/images/instruments/brass/trumpet_1.png/'
up4.save()

pp36 = cmod.ProductPicture()
pp36.product = up4
pp36.path = '/static/homepage/media/images/instruments/brass/trumpet_1.png/'
pp36.save()

pp37 = cmod.ProductPicture()
pp37.product = up4
pp37.path = '/static/homepage/media/images/instruments/brass/trumpet_2.png/'
pp37.save()

pp38 = cmod.ProductPicture()
pp38.product = up4
pp38.path = '/static/homepage/media/images/instruments/brass/trumpet_3.png/'
pp38.save()

up5 = cmod.UniqueProduct()
up5.category = cat1
up5.name = 'Tuba'
up5.brand = 'Accent'
up5.price = Decimal('514.50')
up5.serial_number = 'xyz2'
up5.path = '/static/homepage/media/images/instruments/brass/tuba_1.png/'
up5.save()

pp39 = cmod.ProductPicture()
pp39.product = up5
pp39.path = '/static/homepage/media/images/instruments/brass/tuba_1.png/'
pp39.save()

pp40 = cmod.ProductPicture()
pp40.product = up5
pp40.path = '/static/homepage/media/images/instruments/brass/tuba_2.png/'
pp40.save()

pp40 = cmod.ProductPicture()
pp40.product = up5
pp40.path = '/static/homepage/media/images/instruments/brass/tuba_3.png/'
pp40.save()

up6 = cmod.UniqueProduct()
up6.category = cat3
up6.name = 'Banjo'
up6.brand = 'Accent'
up6.price = Decimal('514.50')
up6.serial_number = 'xyz2'
up6.path = '/static/homepage/media/images/instruments/percussion/banjo_1.png/'
up6.save()

pp41 = cmod.ProductPicture()
pp41.product = up6
pp41.path = '/static/homepage/media/images/instruments/percussion/banjo_1.png/'
pp41.save()

pp42 = cmod.ProductPicture()
pp42.product = up6
pp42.path = '/static/homepage/media/images/instruments/percussion/banjo_2.png/'
pp42.save()

pp43 = cmod.ProductPicture()
pp43.product = up6
pp43.path = '/static/homepage/media/images/instruments/percussion/banjo_3.png/'
pp43.save()

up7 = cmod.UniqueProduct()
up7.category = cat5
up7.name = 'Bass Drum'
up7.brand = 'Accent'
up7.price = Decimal('514.50')
up7.serial_number = 'xyz2'
up7.path = '/static/homepage/media/images/instruments/percussion/bass_drum1.png/'
up7.save()

pp44 = cmod.ProductPicture()
pp44.product = up7
pp44.path = '/static/homepage/media/images/instruments/percussion/bass_drum1.png/'
pp44.save()

pp45 = cmod.ProductPicture()
pp45.product = up7
pp45.path = '/static/homepage/media/images/instruments/percussion/bass_drum2.png/'
pp45.save()

up8 = cmod.UniqueProduct()
up8.category = cat5
up8.name = 'Cymbal'
up8.brand = 'Accent'
up8.price = Decimal('514.50')
up8.serial_number = 'xyz2'
up8.path = '/static/homepage/media/images/instruments/percussion/cymball.png/'
up8.save()

pp46 = cmod.ProductPicture()
pp46.product = up8
pp46.path = '/static/homepage/media/images/instruments/percussion/cymball.png/'
pp46.save()

up9 = cmod.UniqueProduct()
up9.category = cat5
up9.name = 'Gong'
up9.brand = 'Accent'
up9.price = Decimal('514.50')
up9.serial_number = 'xyz2'
up9.path = '/static/homepage/media/images/instruments/percussion/gong.png/'
up9.save()

pp47 = cmod.ProductPicture()
pp47.product = up9
pp47.path = '/static/homepage/media/images/instruments/percussion/gong.png/'
pp47.save()

up10 = cmod.UniqueProduct()
up10.category = cat5
up10.name = 'Snare Drum'
up10.brand = 'Accent'
up10.price = Decimal('514.50')
up10.serial_number = 'xyz2'
up10.path = '/static/homepage/media/images/instruments/percussion/snare_drum1.png/'
up10.save()

pp48 = cmod.ProductPicture()
pp48.product = up10
pp48.path = '/static/homepage/media/images/instruments/percussion/snare_drum1.png/'
pp48.save()

pp49 = cmod.ProductPicture()
pp49.product = up10
pp49.path = '/static/homepage/media/images/instruments/percussion/snare_drum2.png/'
pp49.save()

up11 = cmod.UniqueProduct()
up11.category = cat5
up11.name = 'Tenor Drum'
up11.brand = 'Accent'
up11.price = Decimal('514.50')
up11.serial_number = 'xyz2'
up11.path = '/static/homepage/media/images/instruments/percussion/tenor_drum1.png/'
up11.save()

pp50 = cmod.ProductPicture()
pp50.product = up11
pp50.path = '/static/homepage/media/images/instruments/percussion/tenor_drum1.png/'
pp50.save()

up12 = cmod.UniqueProduct()
up12.category = cat5
up12.name = 'Timpani'
up12.brand = 'Accent'
up12.price = Decimal('514.50')
up12.serial_number = 'xyz2'
up12.path = '/static/homepage/media/images/instruments/percussion/timpani_1.png/'
up12.save()

pp51 = cmod.ProductPicture()
pp51.product = up12
pp51.path = '/static/homepage/media/images/instruments/percussion/timpani_1.png/'
pp51.save()

pp52 = cmod.ProductPicture()
pp52.product = up12
pp52.path = '/static/homepage/media/images/instruments/percussion/timpani_2.png/'
pp52.save()

pp53 = cmod.ProductPicture()
pp53.product = up12
pp53.path = '/static/homepage/media/images/instruments/percussion/timpani_3.png/'
pp53.save()

up13 = cmod.UniqueProduct()
up13.category = cat5
up13.name = 'Xylophone'
up13.brand = 'Accent'
up13.price = Decimal('514.50')
up13.serial_number = 'xyz2'
up13.path = '/static/homepage/media/images/instruments/percussion/xylophone.png/'
up13.save()

pp52 = cmod.ProductPicture()
pp52.product = up13
pp52.path = '/static/homepage/media/images/instruments/percussion/xylophone.png/'
pp52.save()

up14 = cmod.UniqueProduct()
up14.category = cat3
up14.name = 'Acoustic Guitar'
up14.brand = 'Accent'
up14.price = Decimal('514.50')
up14.serial_number = 'xyz2'
up14.path = '/static/homepage/media/images/instruments/string/acoustic_guitar_1.png/'
up14.save()

pp53 = cmod.ProductPicture()
pp53.product = up14
pp53.path = '/static/homepage/media/images/instruments/string/acoustic_guitar_1.png/'
pp53.save()

pp54 = cmod.ProductPicture()
pp54.product = up14
pp54.path = '/static/homepage/media/images/instruments/string/acoustic_guitar_2.png/'
pp54.save()

pp55 = cmod.ProductPicture()
pp55.product = up14
pp55.path = '/static/homepage/media/images/instruments/string/acoustic_guitar_3.png/'
pp55.save()

up15 = cmod.UniqueProduct()
up15.category = cat3
up15.name = 'Bass'
up15.brand = 'Accent'
up15.price = Decimal('514.50')
up15.serial_number = 'xyz2'
up15.path = '/static/homepage/media/images/instruments/string/bass_1.png/'
up15.save()

pp56 = cmod.ProductPicture()
pp56.product = up15
pp56.path = '/static/homepage/media/images/instruments/string/bass_1.png/'
pp56.save()

pp57 = cmod.ProductPicture()
pp57.product = up15
pp57.path = '/static/homepage/media/images/instruments/string/bass_2.png/'
pp57.save()

pp58 = cmod.ProductPicture()
pp58.product = up15
pp58.path = '/static/homepage/media/images/instruments/string/bass_3.png/'
pp58.save()

up16 = cmod.UniqueProduct()
up16.category = cat3
up16.name = 'Bass Guitar'
up16.brand = 'Accent'
up16.price = Decimal('514.50')
up16.serial_number = 'xyz2'
up16.path = '/static/homepage/media/images/instruments/string/bass_guitar_1.png/'
up16.save()

pp59 = cmod.ProductPicture()
pp59.product = up16
pp59.path = '/static/homepage/media/images/instruments/string/bass_guitar_1.png/'
pp59.save()

pp60 = cmod.ProductPicture()
pp60.product = up16
pp60.path = '/static/homepage/media/images/instruments/string/bass_guitar_2.png/'
pp60.save()

pp61 = cmod.ProductPicture()
pp61.product = up16
pp61.path = '/static/homepage/media/images/instruments/string/bass_guitar_3.png/'
pp61.save()

up17 = cmod.UniqueProduct()
up17.category = cat3
up17.name = 'Cello'
up17.brand = 'Accent'
up17.price = Decimal('514.50')
up17.serial_number = 'xyz2'
up17.path = '/static/homepage/media/images/instruments/string/cello_1.png/'
up17.save()

pp62 = cmod.ProductPicture()
pp62.product = up17
pp62.path = '/static/homepage/media/images/instruments/string/cello_1.png/'
pp62.save()

pp63 = cmod.ProductPicture()
pp63.product = up17
pp63.path = '/static/homepage/media/images/instruments/string/cello_2.png/'
pp63.save()

pp64 = cmod.ProductPicture()
pp64.product = up17
pp64.path = '/static/homepage/media/images/instruments/string/cello_3.png/'
pp64.save()

up18 = cmod.UniqueProduct()
up18.category = cat3
up18.name = 'Electric Guitar'
up18.brand = 'Accent'
up18.price = Decimal('514.50')
up18.serial_number = 'xyz2'
up18.path = '/static/homepage/media/images/instruments/string/guitar_1.png/'
up18.save()

pp65 = cmod.ProductPicture()
pp65.product = up18
pp65.path = '/static/homepage/media/images/instruments/string/guitar_1.png/'
pp65.save()

pp66 = cmod.ProductPicture()
pp66.product = up18
pp66.path = '/static/homepage/media/images/instruments/string/guitar_2.png/'
pp66.save()

pp67 = cmod.ProductPicture()
pp67.product = up18
pp67.path = '/static/homepage/media/images/instruments/string/guitar_3.png/'
pp67.save()

up19 = cmod.UniqueProduct()
up19.category = cat3
up19.name = 'Keyboard'
up19.brand = 'Accent'
up19.price = Decimal('514.50')
up19.serial_number = 'xyz2'
up19.path = '/static/homepage/media/images/instruments/string/piano_1.png/'
up19.save()

pp68 = cmod.ProductPicture()
pp68.product = up19
pp68.path = '/static/homepage/media/images/instruments/string/piano_1.png/'
pp68.save()

pp69 = cmod.ProductPicture()
pp69.product = up19
pp69.path = '/static/homepage/media/images/instruments/string/piano_2.png/'
pp69.save()

pp70 = cmod.ProductPicture()
pp70.product = up19
pp70.path = '/static/homepage/media/images/instruments/string/piano_3.png/'
pp70.save()

up20 = cmod.UniqueProduct()
up20.category = cat3
up20.name = 'Viola'
up20.brand = 'Accent'
up20.price = Decimal('514.50')
up20.serial_number = 'xyz2'
up20.path = '/static/homepage/media/images/instruments/string/viola_1.png/'
up20.save()

pp71 = cmod.ProductPicture()
pp71.product = up20
pp71.path = '/static/homepage/media/images/instruments/string/viola_1.png/'
pp71.save()

pp72 = cmod.ProductPicture()
pp72.product = up20
pp72.path = '/static/homepage/media/images/instruments/string/vioal_2.png/'
pp72.save()

pp73 = cmod.ProductPicture()
pp73.product = up20
pp73.path = '/static/homepage/media/images/instruments/string/viola_3.png/'
pp73.save()

up21 = cmod.UniqueProduct()
up21.category = cat3
up21.name = 'Violin'
up21.brand = 'Accent'
up21.price = Decimal('514.50')
up21.serial_number = 'xyz2'
up21.path = '/static/homepage/media/images/instruments/string/violin_1.png/'
up21.save()

pp74 = cmod.ProductPicture()
pp74.product = up21
pp74.path = '/static/homepage/media/images/instruments/string/violin_1.png/'
pp74.save()

pp75 = cmod.ProductPicture()
pp75.product = up21
pp75.path = '/static/homepage/media/images/instruments/string/violin_2.png/'
pp75.save()

pp76 = cmod.ProductPicture()
pp76.product = up21
pp76.path = '/static/homepage/media/images/instruments/string/violin_3.png/'
pp76.save()

up22 = cmod.UniqueProduct()
up22.category = cat2
up22.name = 'Clarinet'
up22.brand = 'Accent'
up22.price = Decimal('514.50')
up22.serial_number = 'xyz2'
up22.path = '/static/homepage/media/images/instruments/woodwind/clarient_1.png/'
up22.save()

pp77 = cmod.ProductPicture()
pp77.product = up22
pp77.path = '/static/homepage/media/images/instruments/woodwind/clarient_1.png/'
pp77.save()

pp78 = cmod.ProductPicture()
pp78.product = up22
pp78.path = '/static/homepage/media/images/instruments/woodwind/clarinet_2.png/'
pp78.save()

up23 = cmod.UniqueProduct()
up23.category = cat2
up23.name = 'Electric Kazoo'
up23.brand = 'Accent'
up23.price = Decimal('514.50')
up23.serial_number = 'xyz2'
up23.path = '/static/homepage/media/images/instruments/woodwind/electric_kazoo.png/'
up23.save()

pp79 = cmod.ProductPicture()
pp79.product = up23
pp79.path = '/static/homepage/media/images/instruments/woodwind/electric_kazoo.png/'
pp79.save()

up24 = cmod.UniqueProduct()
up24.category = cat2
up24.name = 'Flute'
up24.brand = 'Accent'
up24.price = Decimal('514.50')
up24.serial_number = 'xyz2'
up24.path = '/static/homepage/media/images/instruments/woodwind/flute_1.png/'
up24.save()

pp80 = cmod.ProductPicture()
pp80.product = up24
pp80.path = '/static/homepage/media/images/instruments/woodwind/flute_1.png/'
pp80.save()

pp81 = cmod.ProductPicture()
pp81.product = up24
pp81.path = '/static/homepage/media/images/instruments/woodwind/flute_2.png/'
pp81.save()

up25 = cmod.UniqueProduct()
up25.category = cat2
up25.name = 'Harmonica'
up25.brand = 'Accent'
up25.price = Decimal('514.50')
up25.serial_number = 'xyz2'
up25.path = '/static/homepage/media/images/instruments/woodwind/harmonica1.png/'
up25.save()

pp82 = cmod.ProductPicture()
pp82.product = up25
pp82.path = '/static/homepage/media/images/instruments/woodwind/harmonica1.png/'
pp82.save()

pp83 = cmod.ProductPicture()
pp83.product = up25
pp83.path = '/static/homepage/media/images/instruments/woodwind/harmonica2.png/'
pp83.save()

pp84 = cmod.ProductPicture()
pp84.product = up25
pp84.path = '/static/homepage/media/images/instruments/woodwind/harmonica3.png/'
pp84.save()

up26 = cmod.UniqueProduct()
up26.category = cat2
up26.name = 'Oboe'
up26.brand = 'Accent'
up26.price = Decimal('514.50')
up26.serial_number = 'xyz2'
up26.path = '/static/homepage/media/images/instruments/woodwind/oboe_1.png/'
up26.save()

pp85 = cmod.ProductPicture()
pp85.product = up26
pp85.path = '/static/homepage/media/images/instruments/woodwind/oboe_1.png/'
pp85.save()

pp86 = cmod.ProductPicture()
pp86.product = up26
pp86.path = '/static/homepage/media/images/instruments/woodwind/oboe_2.png/'
pp86.save()

up27 = cmod.UniqueProduct()
up27.category = cat2
up27.name = 'Saxophone'
up27.brand = 'Accent'
up27.price = Decimal('514.50')
up27.serial_number = 'xyz2'
up27.path = '/static/homepage/media/images/instruments/woodwind/sax_1.png/'
up27.save()

pp87 = cmod.ProductPicture()
pp87.product = up27
pp87.path = '/static/homepage/media/images/instruments/woodwind/sax_1.png/'
pp87.save()

pp88 = cmod.ProductPicture()
pp88.product = up27
pp88.path = '/static/homepage/media/images/instruments/woodwind/sax_2.png/'
pp88.save()

pp89 = cmod.ProductPicture()
pp89.product = up27
pp89.path = '/static/homepage/media/images/instruments/woodwind/sax_3.png/'
pp89.save()