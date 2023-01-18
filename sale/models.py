from django.db import models
from django.db.models.fields import CharField

# Create Sale models
class Data(models.Model):
    key = models.CharField(max_length=10,primary_key=True)
    value = models.CharField(max_length=100)

class AllProduct(models.Model):
    product_code = models.CharField(max_length=10, primary_key=True)
    product_name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True, blank=True)
    sold_no = models.FloatField(null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    inventory = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = "all_product"
        managed = False
    def __str__(self):
        #return self.product_code 
        return'{"product_code":"%s","product_name":"%s","price":"%s","sold_no":"%s","quantity":%s,"inventory":%s}' % (self.product_code, self.product_name, self.price, self.sold_no, self.quantity, self.inventory)

class Member(models.Model):
    contact = models.CharField(max_length=10, primary_key=True)
    member_id = models.CharField(max_length=7, null=True)
    member_name = models.CharField(max_length=100, null=True)
    member_lname = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = "member"
        managed = False
    def __str__(self):
        #return self.contact
        return'{"contact":"%s","member_id":"%s","member_name":"%s","member_lname":"%s"}' % (self.contact, self.member_id, self.member_name, self.member_lname)
        
class Order(models.Model):
    order_id = models.CharField(max_length=10, primary_key=True)
    order_date = models.DateField(null=True)
    contact = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='contact')
    amount = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = "all_order"
        managed = False
    
    def __str__(self):  
        return "%s %s " % (self.order_id , self.order_date,)   

class OrderLineItem(models.Model):
    order_id = models.ForeignKey(Order, primary_key=True, on_delete=models.CASCADE, db_column='order_id')
    item_no = models.IntegerField()
    product_code = models.ForeignKey(AllProduct, on_delete=models.CASCADE, db_column='product_code')
    quantity = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    product_total = models.FloatField(null=True)
    class Meta:
        db_table = "order_line_item"
        unique_together = (("order_id", "item_no"),)
        managed = False
    def __str__(self):
        return '{"order_id":"%s","iten_no":"%s","product_code":"%s","quantity":%s,"price":"%s","product_total":"%s"}' % (self.order_id, self.item_no, self.product_code, self.quantity, self.price, self.product_total)

  