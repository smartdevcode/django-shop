# -*- coding: utf-8 -*-
from django.db import models
from shop.util.fields import CurrencyField
from django.core.management.validation import max_length

STATUS_CODES = (
    (1, 'Processing'), # User still checking out the contents
    (2, 'Confirmed'), # Contents are valid, now we can handle payment etc...
    (3, 'Completed'), # Everything is fine, only need to send the products
)

class OrderManager(models.Manager):
    
    def create_from_cart(self, cart):
        '''
        This creates a new Order object (and all the rest) from a passed Cart 
        object.
        
        Specifically, it creates an Order with corresponding OrderItems and
        eventually corresponding ExtraPriceFields
        
        '''

class Order(models.Model):
    '''
    A model representing an Order.
    
    An order is the "in process" counterpart of the shopping cart, which holds
    stuff like the shipping and billing addresses (copied from the User profile)
    when the Order is first created), list of items, and holds stuff like the
    status, shipping costs, taxes, etc...
    '''
    
    status = models.IntegerField(choices=STATUS_CODES)
    
    order_subtotal = CurrencyField()
    order_total = CurrencyField()
    
    shipping_cost = CurrencyField()
    
    # Addresses MUST be copied over to the order when it's created.
    shipping_name = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255)
    shipping_zip_code = models.CharField(max_length=20)
    shipping_state = models.CharField(max_length=255)
    shipping_country = models.CharField(max_length=255)
    
    billing_name = models.CharField(max_length=255)
    billingaddress = models.CharField(max_length=255)
    billing_address2 = models.CharField(max_length=255)
    billing_zip_code = models.CharField(max_length=20)
    billing_state = models.CharField(max_length=255)
    billing_country = models.CharField(max_length=255)
    
    class Meta:
        app_label = 'shop'

class OrderItem():
    '''
    A line Item for an order.
    '''
    
    product_name = models.CharField(max_length=255)
    unit_price = CurrencyField()
    quantity = models.IntegerField()
    
    line_subtotal = CurrencyField()
    line_total = CurrencyField()
    
    class Meta:
        app_label = 'shop'
        
class ExtraOrderPriceField(models.Model):
    '''
    This will make Cart-provided extra price fields persistent since we want
    to "snapshot" their statuses at the time when the order was made
    '''
    order = models.ForeignKey(Order)
    label = models.CharField(max_length=255)
    value = CurrencyField()
    
    class Meta:
        app_label = 'shop'
    
class ExtraOrderItemPriceField(models.Model):
    '''
    This will make Cart-provided extra price fields persistent since we want
    to "snapshot" their statuses at the time when the order was made
    '''
    order_item = models.ForeignKey(OrderItem)
    label = models.CharField(max_length=255)
    value = CurrencyField()
    
    class Meta:
        app_label = 'shop'
        