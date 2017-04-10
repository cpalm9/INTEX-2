from django.test import TestCase
from account import models as amod
from datetime import datetime

class AnimalTestCase(TestCase):
    # def setUp(self):
    #     Animal.objects.create(name="lion", sound="roar")
    #     Animal.objects.create(name="cat", sound="meow")

    def test_create_users(self):
        # """Test the creation of a fomouser object"""
        u = amod.FomoUser()
        u.username = 'test1'
        u.first_name = 'Don'
        u.last_name = 'Finnegan'
        u.email = 'test@test.com'
        u.birth_date = datetime(1992, 10, 13)
        u.phone = '636-688-9225'
        u.address = '615 N 100 W'
        u.city = 'Provo'
        u.state = 'UT'
        u.zipcode = '84601'
        u.set_password('password')
        u.is_staff = True
        u.save()
