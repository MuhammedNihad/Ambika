from django import forms
from .models import Product, Size,PlacedOrders,Order,OrderItem
class SizeFilterForm(forms.Form):
  sizes = forms.MultipleChoiceField(choices=Size.SIZE_CHOICES, required=False)

  def filter(self, products):
    if self.cleaned_data['sizes']:
      return products.filter(sizes__in=self.cleaned_data['sizes'])
    else:
      return products
class ProductForm(forms.ModelForm):
    sizes = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,  # Users can select multiple sizes
    )
    class Meta:
        model = Product
        fields = ['name', 'colour_colour', 'specification', 'image','price','overrelayimage','occasions']
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
class PlacedOrdersForm(forms.ModelForm):
    class Meta:
        model = PlacedOrders
        fields = ['address', 'city', 'state', 'zipcode']
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'complete', 'transaction_id']
class ShippingForm(forms.Form):
  """A form for shipping data."""

  city = forms.CharField(max_length=200)
  address = forms.CharField(max_length=200)
  zipcode = forms.CharField(max_length=200)
  state = forms.CharField(max_length=200)
  phone_number=forms.CharField(max_length=15)

