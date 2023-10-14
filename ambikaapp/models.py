from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField



class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    image=models.ImageField(upload_to='categoryimage/',null=True,blank=True)
    def __str__(self) -> str:
        return self.name
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category,null=True,blank=True)
    specification = models.TextField(max_length=2000)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    overrelayimage = models.ImageField(null=True, blank=True)
    colour_colour = ColorField()
    sizes = models.ManyToManyField('Size', through='ProductSize')
    # Define choices for the occasions
    CASUAL_WEAR = 'Casual Wear'
    COMFORT_WEAR = 'Comfort Wear'
    STREET_WEAR = 'Street Wear'
    CLUB_WEAR = 'Club Wear'
    BEACH_WEAR = 'Beach Wear'
    PARTY_WEAR = 'Party Wear'
    HOLIDAY_WEAR = 'Holiday Wear'
    WEEKEND_WEAR = 'Weekend Wear'
    COLLEGE_WEAR = 'College Wear'
    OFFICE_WEAR = 'Office Wear'

    OCCASION_CHOICES = [
        (CASUAL_WEAR, 'Casual Wear'),
        (COMFORT_WEAR, 'Comfort Wear'),
        (STREET_WEAR, 'Street Wear'),
        (CLUB_WEAR, 'Club Wear'),
        (BEACH_WEAR, 'Beach Wear'),
        (PARTY_WEAR, 'Party Wear'),
        (HOLIDAY_WEAR, 'Holiday Wear'),
        (WEEKEND_WEAR, 'Weekend Wear'),
        (COLLEGE_WEAR, 'College Wear'),
        (OFFICE_WEAR, 'Office Wear'),
    ]

    occasions = models.CharField(max_length=20, choices=OCCASION_CHOICES, blank=True, null=True)

    views = models.PositiveIntegerField(default=0)

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
    add_on = models.ManyToManyField("AddOn", related_name="add_ons", blank=True)
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
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    size = models.CharField(max_length=3, choices=Size.SIZE_CHOICES, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    total_amount=models.FloatField(blank=True,null=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)


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

    def __str__(self) -> str:
        return self.title


class AddOn(models.Model):
    """
    Represents an additional item as "add-ons" that can be added to an order item.

    Attributes:
        name (str): The name of the Add-on.
        price (Decimal): The price of the Add-on. If not specified, it defaults to 0.00.
        order_items (ManyToManyField): A many-to-many relationship with the OrderItem model,
            allowing this Add-on to be associated with multiple order items.
    """

    name = models.CharField(_("Name of Add-on"), max_length=255)
    price = models.DecimalField(
        _("Price of Add-on"),
        default=0.00,
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.name}"
