# -*- coding: utf-8 -*-
from __future__ import with_statement
from decimal import Decimal
from django.contrib.auth.models import User
from shop.models.cartmodel import Cart
from shop.models.productmodel import Product
from shop.tests.utils.context_managers import SettingsOverride
from unittest import TestCase

class CartTestCase(TestCase):
    
    def test_01_empty_cart_costs_0(self):
        with SettingsOverride(SHOP_PRICE_MODIFIERS=[]):
            user = User.objects.create(username="test", email="test@example.com")
            
            cart = Cart()
            cart.user = user
            cart.save()
            
            cart.update()
            
            self.assertEqual(cart.subtotal_price, Decimal('0.0'))
            self.assertEqual(cart.total_price, Decimal('0.0'))
            
    def test_02_one_object_no_modifiers(self):
        with SettingsOverride(SHOP_PRICE_MODIFIERS=[]):
            
            the_price = Decimal('12.00')
            
            user = User.objects.create(username="test2", email="test@example.com")
            
            cart = Cart()
            cart.user = user
            cart.save()
            
            product = Product()
            
            product.name = "TestPrduct"
            product.slug = "TestPrduct"
            product.short_description = "TestPrduct"
            product.long_description = "TestPrduct"
            product.active = True
            product.base_price = the_price
            
            product.save()
            
            cart.add_product(product)
            cart.save()
            cart.update()
            cart.save()
            
            self.assertEqual(cart.subtotal_price, the_price)
            self.assertEqual(cart.total_price, the_price)
    
    def test_03_one_object_one_modifier(self):
        pass