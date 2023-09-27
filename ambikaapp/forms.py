from django import forms
from .models import Product, Size,PlacedOrders,Order,OrderItem

class ProductForm(forms.ModelForm):
    sizes = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,  # Users can select multiple sizes
    )
    class Meta:
        model = Product
        fields = ['name', 'colour_colour', 'specification', 'image','price']
    # Optional: Add custom validation logic if needed
    def clean(self):
        cleaned_data = super().clean()
        # Add custom validation logic here if needed
        return cleaned_data
class PlaceOrderForm(forms.Form):
    address = forms.CharField(max_length=200, required=True)
    city = forms.CharField(max_length=200, required=True)
    state = forms.CharField(max_length=200, required=True)
    zipcode = forms.CharField(max_length=200, required=True)
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'complete', 'transaction_id']
