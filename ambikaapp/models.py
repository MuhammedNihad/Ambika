from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    def __str__(self) -> str:
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=200)
    categories=models.ManyToManyField(Category)
    specification = models.TextField(max_length=2000)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    colour_colour = ColorField()
    sizes = models.ManyToManyField('Size', through='ProductSize')
    def __str__(self):
        return self.name
class Size(models.Model):
    SIZE_CHOICES = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        # Add more size choices as needed
    )
    size = models.CharField(max_length=3, choices=SIZE_CHOICES)
    def __str__(self):
        return self.get_size_display()
class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    def __str__(self):
        return f"size: {self.size} Product name :{self.product}"
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    def __str__(self):
        return f"ID:{self.id}Customer name: {self.customer},Date Ordered :{self.date_ordered}"
class OrderItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True) 
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    size = models.CharField(max_length=3, choices=Size.SIZE_CHOICES, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)  # Add a deleted field
    def __str__(self):
        return f"{self.quantity} of {self.product.name} (Size: {self.size})"
class PlacedOrders(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    order_items = models.ManyToManyField(OrderItem, related_name='placed_orders', blank=True)  # Use related_name

    def __str__(self):
        return f"Placed Order ID: {self.id}"

class ProductReview(models.Model):
    order = models.ForeignKey(PlacedOrders, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review_content = models.TextField(max_length=2000)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    def __str__(self):
        return f"Review for {self.product.name} by {self.order.customer}"
class Blog(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    image=models.ImageField(null=True,blank=True)
    conclusion=models.TextField()