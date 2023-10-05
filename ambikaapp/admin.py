from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PlacedOrders)
admin.site.register(ProductReview)
admin.site.register(ProductSize)
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(AddOn)
