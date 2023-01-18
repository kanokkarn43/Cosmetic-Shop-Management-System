from django.db import models
from django.db.models.fields import CharField

# Create Products models
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
        return self.product_code 

