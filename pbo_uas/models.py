from django.db import models


class AgeRange(models.TextChoices):
    A_20 = '1', '<20'
    A_30 = '2', '20-29'
    A_40 = '3', '30-39'
    A_50 = '4', '40-49'
    A_60 = '5', '50-59'
    OTHER = '6', '>60'


class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'


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
    code = models.CharField(max_length=64, default='')
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
    gender = models.CharField(max_length=1 ,choices=Gender.choices)
    age = models.IntegerField(choices=AgeRange.choices)
    date = models.DateField(auto_now_add=True)
    paid = models.IntegerField(null=True)
    payment_method = models.CharField(max_length=32, default=' ')
    change = models.IntegerField(null=True)
    total_amount = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table ='sales'

    @property
    def gender_display(self):
        return self.get_gender_display()

    @property
    def age_display(self):
        return self.get_age_display()


class SaleDetails(models.Model):
    # sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE)
    sale_id = models.IntegerField()
    product_id = models.IntegerField()
    product_category_id = models.IntegerField()
    product_code = models.CharField(max_length=64)
    product_name = models.CharField(max_length=64)
    sold_for = models.IntegerField()
    quantity = models.IntegerField()
    note = models.CharField(max_length=64)

    class Meta:
        db_table ='sale_details'
