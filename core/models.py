from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.shortcuts import reverse

# Create your models here.
GENDER_CHOICES = (
    ('Male','Male'),
    ('Female','Female'),
    ('Unisex','Unisex'),
)
CATEGORY_CHOICES = (
    ('A','Accessories'),
    ('SP','Sport wears'),
    ('O','Outwears'),
)
LABEL_CHOICES = (
    ('P','primary'),
    ('S','secondary'),
    ('D','danger')
)

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    discount_price = models.DecimalField(default=False,max_digits=7,decimal_places=2,blank=True,null=True)
    digital = models.BooleanField(default=False,blank=True,null=True)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=6,blank=True,null=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2,blank=True,null=True)
    label = models.CharField(choices=LABEL_CHOICES,max_length=1,blank=True,null=True)
    images = models.ImageField(upload_to='pics/',blank=True,null=True)
    slug = models.SlugField()
    description = models.TextField(max_length=150)

    def __str__(self):
        return self.name

    @property
    def imageUrl(self):
        try:
            url = self.images.url
        except:
            url =''
        return url
    

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name='Ordered by')
    ordered_date = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False, verbose_name='Is order complete ?')
    transition_id = models.CharField(max_length=150)
    shipping_address = models.ForeignKey('ShippingAddress', related_name="shipping_address",on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.user.username
    
    @property
    def get_cart_total(self):
        order_item = self.orderitem_set.all()
        total = sum([item.get_total for item in order_item])
        return total

    @property
    def get_cart_item(self):
        order_item = self.orderitem_set.all()
        total = sum([item.quantity for item in order_item])
        return total
    
    @property
    def shipping(self):
        shipping = False
        orderitem = self.orderitem_set.all()
        for i in orderitem:
            if i.product.digital == False:
                shipping = True
        return shipping

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    @property
    def get_total(self):
        total = (self.quantity * self.product.price)
        return total
    
    @property
    def get_total_discount(self):
        total = (self.quantity * self.product.discount_price)
        return total
    
    def get_total_save(self):
        total = self.get_total() - self.get_total_discount()
        return total
    
    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount()
        else:
            return self.get_total()



class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    country = CountryField(multiple=False)
    city = models.CharField(max_length=200,null=False)
    zipcode = models.CharField(max_length=200,null=False)
    street_address = models.CharField(max_length=100)
    house_address = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city