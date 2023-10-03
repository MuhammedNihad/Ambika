from django.contrib import admin
from .models import *
class placeddisplay(admin.ModelAdmin):
    list_display=['customer','quantity','total_amount','product','address','date_added']
# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PlacedOrders,placeddisplay)
admin.site.register(ProductReview)
admin.site.register(ProductSize)
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(Blog)

