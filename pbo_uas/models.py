from django.db import models

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=64)
    desc = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'product_categories'

class Product(models.Model):
    name = models.CharField(max_length=64)
    # category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    category_id = models.IntegerField()
    image_path = models.TextField(null=True)
    desc = models.TextField(null=True)
    price = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'products'

class Sale(models.Model):
    sale_no = models.CharField(max_length=32)
    date = models.DateField(auto_now_add=True)
    paid = models.IntegerField(null=True)
    payment_method = models.CharField(max_length=32, default=' ')
    change = models.IntegerField(null=True)
    total_amount = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table ='sales'

class SaleDetails(models.Model):
    # sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE)
    sale_id = models.IntegerField()
    product_id = models.IntegerField()
    product_category_id = models.IntegerField()
    product_name = models.CharField(max_length=64)
    sold_for = models.IntegerField()
    quantity = models.IntegerField()
    note = models.CharField(max_length=64)

    class Meta:
        db_table ='sale_details'
