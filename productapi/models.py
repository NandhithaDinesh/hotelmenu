from django.db import models

# Create your models here.
class Products(models.Model):
    product_name=models.CharField(max_length=120)
    category=models.CharField(max_length=120)
    price=models.IntegerField()
    rating=models.FloatField()

    def __str__(self):
        return self.product_name
