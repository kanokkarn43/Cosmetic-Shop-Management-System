from django.db import models
from django.db.models.fields import CharField

# Create Order models
class Data(models.Model):
    key = models.CharField(max_length=10,primary_key=True)
    value = models.CharField(max_length=100)

class Member(models.Model):
    contact = models.CharField(max_length=10, primary_key=True)
    member_id = models.CharField(max_length=7, null=True)
    member_name = models.CharField(max_length=100, null=True)
    member_lname = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = "member"
        managed = False
    def __str__(self):
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
        return "%s %s %s" % (self.order_id , self.order_date, self.contact)    


          

