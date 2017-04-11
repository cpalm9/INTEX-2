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
bp1.brand = 'Singin Dog'
bp1.price = Decimal('33.99')
bp1.quantity = 20
bp1.reorder_trigger = 5
bp1.reorder_qty = 15
bp1.path = '/static/homepage/media/images/instruments/accessories/bassoon_reed.png'
bp1.desc = "The Singin' Dog Reed is designed for young students or beginners. Medium soft. Hand finished."
bp1.save()

pp1 = cmod.ProductPicture()
pp1.product = bp1
pp1.path = '/static/homepage/media/images/instruments/accessories/bassoon_reed.png'
pp1.save()

pc1 = cmod.ProductComment()
pc1.product_id = 1
pc1.comment = 'Love this instrument!'
pc1.user_id = 1
pc1.save()

bp2 = cmod.BulkProduct()
bp2.category = cat4
bp2.name = 'Drum Sticks'
bp2.brand = 'PROMARK'
bp2.price = Decimal('99.99')
bp2.quantity = 15
bp2.reorder_trigger = 5
bp2.reorder_qty = 10
bp2.path = '/static/homepage/media/images/instruments/accessories/drum_sticks.png'
bp2.desc = "The Pro Mark Drumsticks are quality, balanced sticks made from hand-selected hickory. Hickory offers a great feel with a little bit of flex."
bp2.save()

pp2 = cmod.ProductPicture()
pp2.product = bp2
pp2.path = '/static/homepage/media/images/instruments/accessories/drum_sticks.png'
pp2.save()

bp3 = cmod.BulkProduct()
bp3.category = cat4
bp3.name = 'Electric Guitar String'
bp3.brand = 'Ernie Ball'
bp3.price = Decimal('13.99')
bp3.quantity = 10
bp3.reorder_trigger = 5
bp3.reorder_qty = 5
bp3.path = '/static/homepage/media/images/instruments/accessories/electric_guitar_strings1.png'
bp3.desc = "Ernie Ball Slinky guitar strings are made from nickel-plated steel. They produce a well-balanced all-around good sound."
bp3.save()

pp3 = cmod.ProductPicture()
pp3.product = bp3
pp3.path = '/static/homepage/media/images/instruments/accessories/electric_guitar_strings1.png'
pp3.save()

pp4 = cmod.ProductPicture()
pp4.product = bp3
pp4.path = '/static/homepage/media/images/instruments/accessories/electric_guitar_string2.png'
pp4.save()

bp4 = cmod.BulkProduct()
bp4.category = cat4
bp4.name = 'Guitar Amp'
bp4.brand = 'Marshall'
bp4.price = Decimal('699.99')
bp4.quantity = 10
bp4.reorder_trigger = 5
bp4.reorder_qty = 5
bp4.path = '/static/homepage/media/images/instruments/accessories/guitar_amp.png'
bp4.desc = "The Marshall guitar amp is a tube combo amplifier that is described as a sturdy, all-tube, gig-ready 40-watt workhorse."
bp4.save()

pp5 = cmod.ProductPicture()
pp5.product = bp4
pp5.path = '/static/homepage/media/images/instruments/accessories/guitar_amp.png'
pp5.save()

bp5 = cmod.BulkProduct()
bp5.category = cat4
bp5.name = 'Guitar Picks'
bp5.brand = 'Fender'
bp5.price = Decimal('3.99')
bp5.quantity = 10
bp5.reorder_trigger = 5
bp5.reorder_qty = 5
bp5.path = '/static/homepage/media/images/instruments/accessories/guitar_picks.png'
bp5.desc = "These Fender picks has a special wide body and rounded tip that have become a favorite pick of all types of guitar players."
bp5.save()

pp6 = cmod.ProductPicture()
pp6.product = bp5
pp6.path = '/static/homepage/media/images/instruments/accessories/guitar_picks.png'
pp6.save()

pp7 = cmod.ProductPicture()
pp7.product = bp5
pp7.path = '/static/homepage/media/images/instruments/accessories/guitar_picks_1.png'
pp7.save()

pp8 = cmod.ProductPicture()
pp8.product = bp5
pp8.path = '/static/homepage/media/images/instruments/accessories/guitar_picks_2.png'
pp8.save()

bp6 = cmod.BulkProduct()
bp6.category = cat4
bp6.name = 'Guitar Strap'
bp6.brand = 'Ernie Ball'
bp6.price = Decimal('4.29')
bp6.quantity = 10
bp6.reorder_trigger = 5
bp6.reorder_qty = 5
bp6.path = '/static/homepage/media/images/instruments/accessories/guitar_strap1.png'
bp6.desc = 'The length adjusts from 38" to 68" so anyone can find a comfortable height. This product features a 2" wide Polypropylene webbing material.'
bp6.save()

pp9 = cmod.ProductPicture()
pp9.product = bp6
pp9.path = '/static/homepage/media/images/instruments/accessories/guitar_strap1.png'
pp9.save()

pp10 = cmod.ProductPicture()
pp10.product = bp6
pp10.path = '/static/homepage/media/images/instruments/accessories/guitar_strap2.png'
pp10.save()

pp11 = cmod.ProductPicture()
pp11.product = bp6
pp11.path = '/static/homepage/media/images/instruments/accessories/guitar_strap3.png'
pp11.save()

bp7 = cmod.BulkProduct()
bp7.category = cat4
bp7.name = 'Guitar Strings'
bp7.brand = 'Elixir'
bp7.price = Decimal('12.99')
bp7.quantity = 10
bp7.reorder_trigger = 5
bp7.reorder_qty = 5
bp7.path = '/static/homepage/media/images/instruments/accessories/guitar_strings1.png'
bp7.desc = "These strings are sheathed in a thin polymer coating that retains a natural feel while protecting it from the gunk that shortens their lives."
bp7.save()

pp12 = cmod.ProductPicture()
pp12.product = bp7
pp12.path = '/static/homepage/media/images/instruments/accessories/guitar_strings1.png'
pp12.save()

pp13 = cmod.ProductPicture()
pp13.product = bp7
pp13.path = '/static/homepage/media/images/instruments/accessories/guitar_strings2.png'
pp13.save()

bp8 = cmod.BulkProduct()
bp8.category = cat4
bp8.name = 'Guitar Tuner'
bp8.brand = 'Fishman'
bp8.price = Decimal('27.45')
bp8.quantity = 10
bp8.reorder_trigger = 5
bp8.reorder_qty = 5
bp8.path = '/static/homepage/media/images/instruments/accessories/guitar_tuner.png'
bp8.desc = "This clip-on fully chromatic tuner quickly and accurately finds the note being played and indicates if you are in tune, sharp, or flat."
bp8.save()

pp14 = cmod.ProductPicture()
pp14.product = bp8
pp14.path = '/static/homepage/media/images/instruments/accessories/guitar_tuner.png'
pp14.save()

pp15 = cmod.ProductPicture()
pp15.product = bp8
pp15.path = '/static/homepage/media/images/instruments/accessories/guitar_tuner_2.png'
pp15.save()

bp9 = cmod.BulkProduct()
bp9.category = cat4
bp9.name = 'Music Stand'
bp9.brand = "Musician's Gear"
bp9.price = Decimal('26.99')
bp9.quantity = 10
bp9.reorder_trigger = 5
bp9.reorder_qty = 5
bp9.path = '/static/homepage/media/images/instruments/accessories/music_stand.png'
bp9.desc = "The steel bookplate on the conductor's stand has a return lip with a smooth tilting feature. The bookplate can also be removed from the vertical shaft."
bp9.save()

pp16 = cmod.ProductPicture()
pp16.product = bp9
pp16.path = '/static/homepage/media/images/instruments/accessories/music_stand.png'
pp16.save()

pp17 = cmod.ProductPicture()
pp17.product = bp9
pp17.path = '/static/homepage/media/images/instruments/accessories/music_stand_2.png'
pp17.save()

pp18 = cmod.ProductPicture()
pp18.product = bp9
pp18.path = '/static/homepage/media/images/instruments/accessories/music_stand_3.png'
pp18.save()

bp10 = cmod.BulkProduct()
bp10.category = cat4
bp10.name = 'Oboe Reed'
bp10.brand = 'Stradella'
bp10.price = Decimal('11.61')
bp10.quantity = 10
bp10.reorder_trigger = 5
bp10.reorder_qty = 5
bp10.path = '/static/homepage/media/images/instruments/accessories/oboe_reed.png'
bp10.desc = "Despite being made for students, the quality of these reeds will meet the meticulous expectations of most experienced players."
bp10.save()

pp19 = cmod.ProductPicture()
pp19.product = bp10
pp19.path = '/static/homepage/media/images/instruments/accessories/oboe_reed.png'
pp19.save()

bp11 = cmod.BulkProduct()
bp11.category = cat4
bp11.name = 'Saxophone Mouthpiece'
bp11.brand = 'Berg Larsen'
bp11.price = Decimal('289.99')
bp11.quantity = 10
bp11.reorder_trigger = 5
bp11.reorder_qty = 5
bp11.path = '/static/homepage/media/images/instruments/accessories/saxophone_mouthpiece.png'
bp11.desc = "Berg Larsen stainless steel mouthpieces are known for their increased life and diverse tonal quality."
bp11.save()

pp20 = cmod.ProductPicture()
pp20.product = bp11
pp20.path = '/static/homepage/media/images/instruments/accessories/saxophone_mouthpiece.png'
pp20.save()

bp12 = cmod.BulkProduct()
bp12.category = cat4
bp12.name = 'Saxophone Reeds'
bp12.brand = 'Alexander Reeds'
bp12.price = Decimal('25.10')
bp12.quantity = 10
bp12.reorder_trigger = 5
bp12.reorder_qty = 5
bp12.path = '/static/homepage/media/images/instruments/accessories/saxophone_reeds.png'
bp12.desc = "The Alexander reeds are made of high-grade Southern France cane and have a redesigned tip and profile to project a big and bold sound."
bp12.save()

pp21 = cmod.ProductPicture()
pp21.product = bp12
pp21.path = '/static/homepage/media/images/instruments/accessories/saxophone_reeds.png'
pp21.save()

bp13 = cmod.BulkProduct()
bp13.category = cat4
bp13.name = 'Sheet Music'
bp13.brand = 'G. Schirmer'
bp13.price = Decimal('10.99')
bp13.quantity = 10
bp13.reorder_trigger = 5
bp13.reorder_qty = 5
bp13.path = '/static/homepage/media/images/instruments/accessories/sheet_music_1.png'
bp13.desc = "This is the original Bach music illustrated in a special format for ease of use and enjoyment."
bp13.save()

pp22 = cmod.ProductPicture()
pp22.product = bp13
pp22.path = '/static/homepage/media/images/instruments/accessories/sheet_music_1.png'
pp22.save()

pp23 = cmod.ProductPicture()
pp23.product = bp13
pp23.path = '/static/homepage/media/images/instruments/accessories/sheet_music_2.png'
pp23.save()

pp24 = cmod.ProductPicture()
pp24.product = bp13
pp24.path = '/static/homepage/media/images/instruments/accessories/sheet_music_3.png'
pp24.save()

bp14 = cmod.BulkProduct()
bp14.category = cat4
bp14.name = 'Trumpet Mouthpiece'
bp14.brand = 'Bach Standard'
bp14.price = Decimal('56.00')
bp14.quantity = 10
bp14.reorder_trigger = 5
bp14.reorder_qty = 5
bp14.path = '/static/homepage/media/images/instruments/accessories/trumpet_mouthpiece.png'
bp14.desc = "Bach mouthpieces are some of the most popular mouthpieces in the world for their special tone and design."
bp14.save()

pp25 = cmod.ProductPicture()
pp25.product = bp14
pp25.path = '/static/homepage/media/images/instruments/accessories/trumpet_mouthpiece.png'
pp25.save()

bp15 = cmod.BulkProduct()
bp15.category = cat4
bp15.name = 'Trumpet Mute'
bp15.brand = 'Harmon'
bp15.price = Decimal('37.99')
bp15.quantity = 10
bp15.reorder_trigger = 5
bp15.reorder_qty = 5
bp15.path = '/static/homepage/media/images/instruments/accessories/trumpet_mute1.png'
bp15.desc = "This special mute is created entirely from aluminum. It is a free-blowing mute that will not alter or change the pitch in any way."
bp15.save()

pp26 = cmod.ProductPicture()
pp26.product = bp15
pp26.path = '/static/homepage/media/images/instruments/accessories/trumpet_mute1.png'
pp26.save()

pp27 = cmod.ProductPicture()
pp27.product = bp15
pp27.path = '/static/homepage/media/images/instruments/accessories/trumpet_mute2.png'
pp27.save()

######################## Unique Products ##########################################
up1 = cmod.UniqueProduct()
up1.category = cat1
up1.name = 'French Horn'
up1.brand = 'Allora'
up1.price = Decimal('1599.99')
up1.serial_number = 'fh001'
up1.path = '/static/homepage/media/images/instruments/brass/double_1.png'
up1.desc = "This special French Horn combines both amazing performance an affordable price. Specially designed for excellent response and tone."
up1.save()

pp28 = cmod.ProductPicture()
pp28.product = up1
pp28.path = '/static/homepage/media/images/instruments/brass/double_1.png'
pp28.save()

pp29 = cmod.ProductPicture()
pp29.product = up1
pp29.path = '/static/homepage/media/images/instruments/brass/double_2.png'
pp29.save()

up2 = cmod.UniqueProduct()
up2.category = cat1
up2.name = 'Fluglehorn'
up2.brand = 'B&S'
up2.price = Decimal('2371.00')
up2.serial_number = 'fh002'
up2.path = '/static/homepage/media/images/instruments/brass/flugelhorn_1.png'
up2.desc = "The B&S fluglehorn has a great value that produces a flexible and fat tone that all musicians seek."
up2.save()

pp30 = cmod.ProductPicture()
pp30.product = up2
pp30.path = '/static/homepage/media/images/instruments/brass/flugelhorn_1.png'
pp30.save()

pp31 = cmod.ProductPicture()
pp31.product = up2
pp31.path = '/static/homepage/media/images/instruments/brass/flugelhron_2.png'
pp31.save()

pp32 = cmod.ProductPicture()
pp32.product = up2
pp32.path = '/static/homepage/media/images/instruments/brass/flugelhron_3.png'
pp32.save()

up3 = cmod.UniqueProduct()
up3.category = cat1
up3.name = 'Trombone'
up3.brand = 'Prelude'
up3.price = Decimal('1039.00')
up3.serial_number = 'trb001'
up3.path = '/static/homepage/media/images/instruments/brass/trombone_1.png'
up3.desc = "The Prelude trombone is a high-quality student symphonic trombone that is appropriate for any type of music including smooth jazz and quick pop."
up3.save()

pp33 = cmod.ProductPicture()
pp33.product = up3
pp33.path = '/static/homepage/media/images/instruments/brass/trombone_1.png'
pp33.save()

pp34 = cmod.ProductPicture()
pp34.product = up3
pp34.path = '/static/homepage/media/images/instruments/brass/trombone_2.png'
pp34.save()

pp35 = cmod.ProductPicture()
pp35.product = up3
pp35.path = '/static/homepage/media/images/instruments/brass/trombone_3.png'
pp35.save()

up4 = cmod.UniqueProduct()
up4.category = cat1
up4.name = 'Trumpet'
up4.brand = 'Allora'
up4.price = Decimal('599.99')
up4.serial_number = 'tr001'
up4.path = '/static/homepage/media/images/instruments/brass/trumpet_1.png'
up4.desc = "This amazing instrument offers a professional-level quality at an affordable price. It is used in any type of music from concert to jazz."
up4.save()

pp36 = cmod.ProductPicture()
pp36.product = up4
pp36.path = '/static/homepage/media/images/instruments/brass/trumpet_1.png'
pp36.save()

pp37 = cmod.ProductPicture()
pp37.product = up4
pp37.path = '/static/homepage/media/images/instruments/brass/trumpet_2.png'
pp37.save()

pp38 = cmod.ProductPicture()
pp38.product = up4
pp38.path = '/static/homepage/media/images/instruments/brass/trumpet_3.png'
pp38.save()

up5 = cmod.UniqueProduct()
up5.category = cat1
up5.name = 'Tuba'
up5.brand = 'Amati'
up5.price = Decimal('3259.00')
up5.serial_number = 'tb001'
up5.path = '/static/homepage/media/images/instruments/brass/tuba_1.png'
up5.desc = "The Amatia Tuba is loved by tuba players worldwide for its round sound and consistent playability amoung all players."
up5.save()

pp39 = cmod.ProductPicture()
pp39.product = up5
pp39.path = '/static/homepage/media/images/instruments/brass/tuba_1.png'
pp39.save()

pp40 = cmod.ProductPicture()
pp40.product = up5
pp40.path = '/static/homepage/media/images/instruments/brass/tuba_2.png'
pp40.save()

pp40 = cmod.ProductPicture()
pp40.product = up5
pp40.path = '/static/homepage/media/images/instruments/brass/tuba_3.png'
pp40.save()

up6 = cmod.UniqueProduct()
up6.category = cat3
up6.name = 'Banjo'
up6.brand = 'Rogue'
up6.price = Decimal('199.99')
up6.serial_number = 'bj001'
up6.path = '/static/homepage/media/images/instruments/percussion/banjo_1.png'
up6.desc = "The Rogue Banjo is known for its amazing sounds of the South at a great and low price."
up6.save()

pp41 = cmod.ProductPicture()
pp41.product = up6
pp41.path = '/static/homepage/media/images/instruments/percussion/banjo_1.png'
pp41.save()

pp42 = cmod.ProductPicture()
pp42.product = up6
pp42.path = '/static/homepage/media/images/instruments/percussion/banjo_2.png'
pp42.save()

pp43 = cmod.ProductPicture()
pp43.product = up6
pp43.path = '/static/homepage/media/images/instruments/percussion/banjo_3.png'
pp43.save()

up7 = cmod.UniqueProduct()
up7.category = cat5
up7.name = 'Bass Drum'
up7.brand = 'SPL'
up7.price = Decimal('779.99')
up7.serial_number = 'bdr001'
up7.path = '/static/homepage/media/images/instruments/percussion/bass_drum1.png'
up7.desc = "SPL Bass Drums provide a balanced tone with low-end projection to match that of the high frequencies produced by smaller drums."
up7.save()

pp44 = cmod.ProductPicture()
pp44.product = up7
pp44.path = '/static/homepage/media/images/instruments/percussion/bass_drum1.png'
pp44.save()

pp45 = cmod.ProductPicture()
pp45.product = up7
pp45.path = '/static/homepage/media/images/instruments/percussion/bass_drum2.png'
pp45.save()

up8 = cmod.UniqueProduct()
up8.category = cat5
up8.name = 'Cymbal'
up8.brand = 'Zildijan'
up8.price = Decimal('309.95')
up8.serial_number = 'cy001'
up8.path = '/static/homepage/media/images/instruments/percussion/cymball.png'
up8.desc = "From the world leading brand for cymbals, Zildijian has created this cymbal that offers a sweet and crisp sound essential to any band."
up8.save()

pp46 = cmod.ProductPicture()
pp46.product = up8
pp46.path = '/static/homepage/media/images/instruments/percussion/cymball.png'
pp46.save()

up9 = cmod.UniqueProduct()
up9.category = cat5
up9.name = 'Gong'
up9.brand = 'Zildijian'
up9.price = Decimal('399.99')
up9.serial_number = 'g001'
up9.path = '/static/homepage/media/images/instruments/percussion/gong.png'
up9.desc = "Hand-hammered and crafted to old-world specifications, the Zildijian Gong is specially created for a classic gong sound."
up9.save()

pp47 = cmod.ProductPicture()
pp47.product = up9
pp47.path = '/static/homepage/media/images/instruments/percussion/gong.png'
pp47.save()

up10 = cmod.UniqueProduct()
up10.category = cat5
up10.name = 'Snare Drum'
up10.brand = 'Ludwig'
up10.price = Decimal('849.00')
up10.serial_number = 'sd001'
up10.path = '/static/homepage/media/images/instruments/percussion/snare_drum1.png'
up10.desc = "This snare drum features chrome metal shell construction that offers a bright, cutting, and crisp sound."
up10.save()

pp48 = cmod.ProductPicture()
pp48.product = up10
pp48.path = '/static/homepage/media/images/instruments/percussion/snare_drum1.png'
pp48.save()

pp49 = cmod.ProductPicture()
pp49.product = up10
pp49.path = '/static/homepage/media/images/instruments/percussion/snare_drum2.png'
pp49.save()

up11 = cmod.UniqueProduct()
up11.category = cat5
up11.name = 'Tenor Drum'
up11.brand = 'Tama'
up11.price = Decimal('429.99')
up11.serial_number = 'td001'
up11.path = '/static/homepage/media/images/instruments/percussion/tenor_drum1.png'
up11.desc = "These special tenor drums feature 8-ply mahogany and beech shells that have a balanced warmth with punch and strength."
up11.save()

pp50 = cmod.ProductPicture()
pp50.product = up11
pp50.path = '/static/homepage/media/images/instruments/percussion/tenor_drum1.png'
pp50.save()

up12 = cmod.UniqueProduct()
up12.category = cat5
up12.name = 'Timpani'
up12.brand = 'Ludwig'
up12.price = Decimal('1659.99')
up12.serial_number = 'ti001'
up12.path = '/static/homepage/media/images/instruments/percussion/timpani_1.png'
up12.desc = "Ludwig Timpani drums are special drums that create a balanced and clean sound essential to every orchestra and symphony."
up12.save()

pp51 = cmod.ProductPicture()
pp51.product = up12
pp51.path = '/static/homepage/media/images/instruments/percussion/timpani_1.png'
pp51.save()

pp52 = cmod.ProductPicture()
pp52.product = up12
pp52.path = '/static/homepage/media/images/instruments/percussion/timpani_2.png'
pp52.save()

pp53 = cmod.ProductPicture()
pp53.product = up12
pp53.path = '/static/homepage/media/images/instruments/percussion/timpani_3.png'
pp53.save()

up13 = cmod.UniqueProduct()
up13.category = cat5
up13.name = 'Xylophone'
up13.brand = 'Sound Percussion'
up13.price = Decimal('499.99')
up13.serial_number = 'x001'
up13.path = '/static/homepage/media/images/instruments/percussion/xylophone.png'
up13.desc = "This xylophone is an excellent choice for the beginning mallet player as well as a superior tool for home practice for the experienced player."
up13.save()

pp52 = cmod.ProductPicture()
pp52.product = up13
pp52.path = '/static/homepage/media/images/instruments/percussion/xylophone.png'
pp52.save()

up14 = cmod.UniqueProduct()
up14.category = cat3
up14.name = 'Acoustic Guitar'
up14.brand = 'Rogue'
up14.price = Decimal('69.99')
up14.serial_number = 'ag001'
up14.path = '/static/homepage/media/images/instruments/string/acoustic_guitar_1.png'
up14.desc = "The Rogue acoustic guitar is a perfect choice for the beginner or young musician. The tons produced by this instrument fill the room with a special sound."
up14.save()

pp53 = cmod.ProductPicture()
pp53.product = up14
pp53.path = '/static/homepage/media/images/instruments/string/acoustic_guitar_1.png'
pp53.save()

pp54 = cmod.ProductPicture()
pp54.product = up14
pp54.path = '/static/homepage/media/images/instruments/string/acoustic_guitar_2.png'
pp54.save()

pp55 = cmod.ProductPicture()
pp55.product = up14
pp55.path = '/static/homepage/media/images/instruments/string/acoustic_guitar_3.png'
pp55.save()

up15 = cmod.UniqueProduct()
up15.category = cat3
up15.name = 'Double Bass'
up15.brand = 'Stentor'
up15.price = Decimal('1539.99')
up15.serial_number = 'db001'
up15.path = '/static/homepage/media/images/instruments/string/bass_1.png'
up15.desc = "The Stentor Student double bass is made to a high standard and offers good playability at an affordable price."
up15.save()

pp56 = cmod.ProductPicture()
pp56.product = up15
pp56.path = '/static/homepage/media/images/instruments/string/bass_1.png'
pp56.save()

pp57 = cmod.ProductPicture()
pp57.product = up15
pp57.path = '/static/homepage/media/images/instruments/string/bass_2.png'
pp57.save()

pp58 = cmod.ProductPicture()
pp58.product = up15
pp58.path = '/static/homepage/media/images/instruments/string/bass_3.png'
pp58.save()

up16 = cmod.UniqueProduct()
up16.category = cat3
up16.name = 'Bass Guitar'
up16.brand = 'Fender'
up16.price = Decimal('699.99')
up16.serial_number = 'bg001'
up16.path = '/static/homepage/media/images/instruments/string/bass_guitar_1.png'
up16.desc = "This Fender guitar is for the modern bassist who demands a cutting-edge tone along with timeless style and a smooth, fast playing feel."
up16.save()

pp59 = cmod.ProductPicture()
pp59.product = up16
pp59.path = '/static/homepage/media/images/instruments/string/bass_guitar_1.png'
pp59.save()

pp60 = cmod.ProductPicture()
pp60.product = up16
pp60.path = '/static/homepage/media/images/instruments/string/bass_guitar_2.png'
pp60.save()

pp61 = cmod.ProductPicture()
pp61.product = up16
pp61.path = '/static/homepage/media/images/instruments/string/bass_guitar_3.png'
pp61.save()

up17 = cmod.UniqueProduct()
up17.category = cat3
up17.name = 'Cello'
up17.brand = 'Bellafina'
up17.price = Decimal('799.99')
up17.serial_number = 'ce001'
up17.path = '/static/homepage/media/images/instruments/string/cello_1.png'
up17.desc = "The Bellafina features a hand-select spruce top, maple back and sides, and an all-ebony fingerboard and pegs."
up17.save()

pp62 = cmod.ProductPicture()
pp62.product = up17
pp62.path = '/static/homepage/media/images/instruments/string/cello_1.png'
pp62.save()

pp63 = cmod.ProductPicture()
pp63.product = up17
pp63.path = '/static/homepage/media/images/instruments/string/cello_2.png'
pp63.save()

pp64 = cmod.ProductPicture()
pp64.product = up17
pp64.path = '/static/homepage/media/images/instruments/string/cello_3.png'
pp64.save()

up18 = cmod.UniqueProduct()
up18.category = cat3
up18.name = 'Electric Guitar'
up18.brand = 'Gibson'
up18.price = Decimal('2269.00')
up18.serial_number = 'eg001'
up18.path = '/static/homepage/media/images/instruments/string/guitar_1.png'
up18.desc = "This beautiful piece of art is created with Ultra-Modern weight technology that allows for comfortable play and greater sonic depth."
up18.save()

pp65 = cmod.ProductPicture()
pp65.product = up18
pp65.path = '/static/homepage/media/images/instruments/string/guitar_1.png'
pp65.save()

pp66 = cmod.ProductPicture()
pp66.product = up18
pp66.path = '/static/homepage/media/images/instruments/string/guitar_2.png'
pp66.save()

pp67 = cmod.ProductPicture()
pp67.product = up18
pp67.path = '/static/homepage/media/images/instruments/string/guitar_3.png'
pp67.save()

up19 = cmod.UniqueProduct()
up19.category = cat3
up19.name = 'Keyboard'
up19.brand = 'Williams Allegro'
up19.price = Decimal('299.99')
up19.serial_number = 'xyz2'
up19.path = '/static/homepage/media/images/instruments/string/piano_1.png'
up19.desc = "The Williams Allegro keyboard is a full-size digital piano with 88 hammer action weighted keys and a brilliant new custom sound library."
up19.save()

pp68 = cmod.ProductPicture()
pp68.product = up19
pp68.path = '/static/homepage/media/images/instruments/string/piano_1.png'
pp68.save()

pp69 = cmod.ProductPicture()
pp69.product = up19
pp69.path = '/static/homepage/media/images/instruments/string/piano_2.png'
pp69.save()

pp70 = cmod.ProductPicture()
pp70.product = up19
pp70.path = '/static/homepage/media/images/instruments/string/piano_3.png'
pp70.save()

up20 = cmod.UniqueProduct()
up20.category = cat3
up20.name = 'Viola'
up20.brand = 'Ren Wei Shi'
up20.price = Decimal('599.99')
up20.serial_number = 'va001'
up20.path = '/static/homepage/media/images/instruments/string/viola_1.png'
up20.desc = "This instrument was designed to offer a solid foundation to the advancing player but still at an affordable price."
up20.save()

pp71 = cmod.ProductPicture()
pp71.product = up20
pp71.path = '/static/homepage/media/images/instruments/string/viola_1.png'
pp71.save()

pp72 = cmod.ProductPicture()
pp72.product = up20
pp72.path = '/static/homepage/media/images/instruments/string/vioal_2.png'
pp72.save()

pp73 = cmod.ProductPicture()
pp73.product = up20
pp73.path = '/static/homepage/media/images/instruments/string/viola_3.png'
pp73.save()

up21 = cmod.UniqueProduct()
up21.category = cat3
up21.name = 'Violin'
up21.brand = 'Bellafina'
up21.price = Decimal('199.99')
up21.serial_number = 'vn001'
up21.path = '/static/homepage/media/images/instruments/string/violin_1.png'
up21.desc = "The Bellafina is a beautiful violin that starts with a hand-selected spruce top, maple back and sides, and an all-ebony fingerboard and pegs."
up21.save()

pp74 = cmod.ProductPicture()
pp74.product = up21
pp74.path = '/static/homepage/media/images/instruments/string/violin_1.png'
pp74.save()

pp75 = cmod.ProductPicture()
pp75.product = up21
pp75.path = '/static/homepage/media/images/instruments/string/violin_2.png'
pp75.save()

pp76 = cmod.ProductPicture()
pp76.product = up21
pp76.path = '/static/homepage/media/images/instruments/string/violin_3.png'
pp76.save()

up22 = cmod.UniqueProduct()
up22.category = cat2
up22.name = 'Clarinet'
up22.brand = 'Etude'
up22.price = Decimal('149.99')
up22.serial_number = 'ct001'
up22.path = '/static/homepage/media/images/instruments/woodwind/clarient_1.png'
up22.desc = "The Etude clarinet offers a sturdy construction with a classic look and sound."
up22.save()

pp77 = cmod.ProductPicture()
pp77.product = up22
pp77.path = '/static/homepage/media/images/instruments/woodwind/clarient_1.png'
pp77.save()

pp78 = cmod.ProductPicture()
pp78.product = up22
pp78.path = '/static/homepage/media/images/instruments/woodwind/clarinet_2.png'
pp78.save()

up23 = cmod.UniqueProduct()
up23.category = cat2
up23.name = 'Electric Kazoo'
up23.brand = 'Lyons Hummbucker'
up23.price = Decimal('16.95')
up23.serial_number = 'ek001'
up23.path = '/static/homepage/media/images/instruments/woodwind/electric_kazoo.png'
up23.desc = "This fun instrument is built with the best materials to create a great sound that can fill a concert hall."
up23.save()

pp79 = cmod.ProductPicture()
pp79.product = up23
pp79.path = '/static/homepage/media/images/instruments/woodwind/electric_kazoo.png'
pp79.save()

up24 = cmod.UniqueProduct()
up24.category = cat2
up24.name = 'Flute'
up24.brand = 'Yamaha'
up24.price = Decimal('1205.99')
up24.serial_number = 'fl001'
up24.path = '/static/homepage/media/images/instruments/woodwind/flute_1.png'
up24.desc = "Yamaha flutes are designed from the outset as student instruments that accommodate the particular needs of a beginning player."
up24.save()

pp80 = cmod.ProductPicture()
pp80.product = up24
pp80.path = '/static/homepage/media/images/instruments/woodwind/flute_1.png'
pp80.save()

pp81 = cmod.ProductPicture()
pp81.product = up24
pp81.path = '/static/homepage/media/images/instruments/woodwind/flute_2.png'
pp81.save()

up25 = cmod.UniqueProduct()
up25.category = cat2
up25.name = 'Harmonica'
up25.brand = 'Lee Oskar'
up25.price = Decimal('37.99')
up25.serial_number = 'har001'
up25.path = '/static/homepage/media/images/instruments/woodwind/harmonica1.png'
up25.desc = "This harmonica is well-suited for blues, rock, country, folk, and jazz. It is more airtight, easier to bend, and better sounding than any other competitor."
up25.save()

pp82 = cmod.ProductPicture()
pp82.product = up25
pp82.path = '/static/homepage/media/images/instruments/woodwind/harmonica1.png'
pp82.save()

pp83 = cmod.ProductPicture()
pp83.product = up25
pp83.path = '/static/homepage/media/images/instruments/woodwind/harmonica2.png'
pp83.save()

pp84 = cmod.ProductPicture()
pp84.product = up25
pp84.path = '/static/homepage/media/images/instruments/woodwind/harmonica3.png'
pp84.save()

up26 = cmod.UniqueProduct()
up26.category = cat2
up26.name = 'Oboe'
up26.brand = 'Bulgheroni'
up26.price = Decimal('5895.00')
up26.serial_number = 'ob001'
up26.path = '/static/homepage/media/images/instruments/woodwind/oboe_1.png'
up26.desc = "The highest wood quality, heavily silver plated keys, artistic keywork along with magnificent tone make Bulgheroni instruments truly world class."
up26.save()

pp85 = cmod.ProductPicture()
pp85.product = up26
pp85.path = '/static/homepage/media/images/instruments/woodwind/oboe_1.png'
pp85.save()

pp86 = cmod.ProductPicture()
pp86.product = up26
pp86.path = '/static/homepage/media/images/instruments/woodwind/oboe_2.png'
pp86.save()

up27 = cmod.UniqueProduct()
up27.category = cat2
up27.name = 'Saxophone'
up27.brand = 'Etude'
up27.price = Decimal('299.99')
up27.serial_number = 'sx001'
up27.path = '/static/homepage/media/images/instruments/woodwind/sax_1.png'
up27.desc = "This is the perfect instrument for a beginner. The keywork, pads, and adjustment all work together to make the tone more consistent and stronger."
up27.save()

pp87 = cmod.ProductPicture()
pp87.product = up27
pp87.path = '/static/homepage/media/images/instruments/woodwind/sax_1.png'
pp87.save()

pp88 = cmod.ProductPicture()
pp88.product = up27
pp88.path = '/static/homepage/media/images/instruments/woodwind/sax_2.png'
pp88.save()

pp89 = cmod.ProductPicture()
pp89.product = up27
pp89.path = '/static/homepage/media/images/instruments/woodwind/sax_3.png'
pp89.save()