from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import json
import twilio.rest as twilio
import random
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import RegexValidator
# Create your views here.
from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,OrderItem,Order,PlacedOrders,Blog,Customer
from .forms import ProductForm,PlaceOrderForm,PlacedOrdersForm,ShippingForm
import os 
from twilio.rest import Client
TWILIO_ACCOUNT_SID="AC2aafc7bcbd200fc8adac03cfa8bc8510"
TWILIO_AUTH_TOKEN="3064482eac918f7e5054b5054f887541"
client=Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
def generate_random_otp():
    # Generate a random 6-digit OTP code
    otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return otp_code
def send_sms_verification(request):
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            # Generate a random OTP code (you can implement this logic)
            otp_code = generate_random_otp()

            # Send the OTP via Twilio
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f'Your OTP code is: {otp_code}',
                from_="+12565738031",
                to=phone_number
            )

            request.session['otp_code'] = otp_code
            request.session['phone_number'] = phone_number
            request.session['address'] = address
            request.session['city'] = city
            request.session['state'] = state
            request.session['zipcode'] = zipcode

            return redirect('place_order')  

    else:
        form = ShippingForm()

    return render(request, 'phone_verification.html', {'form': form})
@csrf_exempt
def sendsms(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        customer = request.POST.get('customer')
        code = request.POST.get('code')
        
        if phone_number and customer and code:
            print("working sms")
            message = client.messages.create(
                body=f"hi {customer} your verification code is {code}",
                from_="+12565738031",
                to=phone_number
            )
            return HttpResponse("SMS sent successfully")
        else:
            return HttpResponse("Missing required data in the request", status=400)
    else:
        return HttpResponse("Invalid request method", status=405)

def all_products(request):
    products = Product.objects.all()#get all products
    return render(request, 'all_products.html', {'products': products})
def trending_page(request):
    # Get a list of products ordered by the 'views' field in descending order
    products = Product.objects.order_by('-views')

    return render(request, 'trending_page.html', {'products': products})
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():#validating the code
            product = form.save()  # Save the basic product details
            sizes = request.POST.getlist('sizes')  # Get the selected sizes from the form
            product.sizes.set(sizes)  # Assign the selected sizes to the product
            return redirect('all_products')  # Redirect to a page displaying all products
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})
def single_product(request, product_id):
    try:
        selected_product = get_object_or_404(Product,pk=product_id)
        selected_product.views=selected_product.views+1
        selected_size = request.GET.get('size')
        selected_product.save()
    except Product.DoesNotExist:
        # Handle the case where the product doesn't exist
        selected_product = None
        selected_size = None

    context = {
        'product': selected_product,
        'selected_size': selected_size,
    }

    return render(request, 'single_product.html', context)
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        action = data.get('action')
        size = data.get('size')
        quantity = data.get('quantity')
        if request.user.is_authenticated:
            customer = request.user.customer
            product = Product.objects.get(id=product_id)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product,size=size,quantity=quantity)
            if action == 'add':
                order_item.customer=customer
                if not item_created:
                    order_item.quantity = quantity
                order_item.save()
            elif action == 'remove':
                order_item.delete()
        else:
            cart = request.session.get('cart', {})

            if action == 'add':
                if product_id not in cart:
                    cart[product_id] = {'quantity': quantity, 'size': size}
                else:
                    quantity+=quantity+1
                    cart[product_id]={'quantity':quantity,'size':size}
            elif action == 'remove':
                if product_id in cart and cart[product_id]['size'] == size:
                    del cart[product_id]
            elif action=="increment":
                print("increament")

            request.session['cart'] = cart

        response_data = {'message': 'Product updated in cart successfully'}
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'})
def cart(request, action=None):
    if request.user.is_authenticated:
        # User is authenticated, retrieve cart items associated with the user
        user = request.user
        cart, created = Order.objects.get_or_create(customer=user.customer, complete=False)
        order_items = cart.orderitem_set.all()
        total_amount = sum(item.product.price * item.quantity for item in order_items)
    else:
        # User is not authenticated, retrieve cart items from the session
        cart = request.session.get('cart', {})
        order_items = []

        for product_id, item_data in cart.items():
            product = get_object_or_404(Product, pk=product_id)
            quantity = item_data.get('quantity', 0)
            size = item_data.get('size', '')
            order_items.append({
                'product': product,
                'quantity': quantity,
                'size': size,
                'total_price': product.price * quantity,
            })

        total_amount = sum(item['total_price'] for item in order_items)

    if action == 'increment':
        product_id = request.POST.get('product_id')
        order_item = get_object_or_404(OrderItem, pk=product_id)

        # Increment the quantity by 1
        order_item.quantity += 1
        order_item.save()
        cart = request.session.get('cart', {})
        cart[product_id] = {'size': size, 'quantity': quantity}
        request.session['cart'] = cart

        return JsonResponse({'message': 'Quantity incremented successfully.'})

    elif action == 'decrement':
        product_id = request.POST.get('product_id')
        order_item = get_object_or_404(OrderItem, pk=product_id)

        # Decrement the quantity by 1 if it's greater than 0
        if order_item.quantity > 0:
            order_item.quantity -= 1
            order_item.save()
            return JsonResponse({'message': 'Quantity decremented successfully.'})
        else:
            return JsonResponse({'message': 'Quantity is already at the minimum.'})

    elif action == 'add':
        product_id = request.POST.get('product_id')
        size = request.POST.get('size')
        quantity = request.POST.get('quantity')

        # Add the product to the session cart
        cart = request.session.get('cart', {})
        cart[product_id] = {'size': size, 'quantity': quantity}
        request.session['cart'] = cart

        return JsonResponse({'message': 'Product added to cart successfully.'})

    elif action == 'remove':
        product_id = request.POST.get('product_id')

        # Remove the product from the session cart
        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
            return JsonResponse({'message': 'Product removed from cart successfully.'})

    context = {
        'order_items': order_items,
        'total_amount': total_amount,
    }

    return render(request, 'cart.html', context)
def update_quantity(request):
    if request.method == 'POST':
        # Extract data from the AJAX request
        data = json.loads(request.body.decode('utf-8'))
        item_id = data.get('id')
        new_quantity = data.get('quantity')
        customer = request.user.customer        
        # Check if the user is authenticated
        if customer=="AnonymousUser":
            print("anonymous")
        if request.user.is_authenticated:
            try:
                # Retrieve the OrderItem instance by its ID
                order_item = OrderItem.objects.get(pk=item_id)

                order_item.quantity = new_quantity
                order_item.customer = customer

                if order_item.quantity <= 0:
                    order_item.delete()  # Remove the item if quantity is zero or less
                else:
                    customer=request.user.customer
                    order_item.save()

                response_data = {
                    'success': True,
                    'message': 'Quantity updated successfully.',
                }
                return JsonResponse(response_data)

            except OrderItem.DoesNotExist:
                response_data = {
                    'success': False,
                    'message': 'OrderItem not found.',
                }
                return JsonResponse(response_data, status=404)
        if not request.user.is_authenticated:
            print("this is anony")
            # If the user is not authenticated, update the session cart
            cart = request.session.get('cart', {})
            if item_id in cart:
                if new_quantity <= 0:
                    del cart[item_id]  # Remove the item if quantity is zero or less
                else:
                    cart[item_id]['quantity'] = new_quantity
                request.session['cart'] = cart
                response_data = {
                    'success': True,
                    'message': 'Quantity updated successfully.',
                }
                return JsonResponse(response_data)
            else:
                response_data = {
                    'success': False,
                    'message': 'Item not found in the cart.',
                }
                return JsonResponse(response_data, status=404)

class PhoneNumberVerifier:
  def __init__(self, client):
    self.client = client

  def send_verification_code(self, phone_number):
    global verification_sid
    verification = self.client.verify.services('VA0b78d24c38c1157639504d911919d1fc').verifications.create(
        to=phone_number,
        channel='sms'
    )

    verification_sid = verification.sid

  def verify_phone_number(self, phone_number, verification_code):
    verification_check = self.client.verify.services('VA0b78d24c38c1157639504d911919d1fc').verifications.check(
        verification_sid=verification_sid,
        code=verification_code
    )

    return verification_check.status == 'approved'


verification_sid = None
def place_order(request):
    otp_code = request.session.get('otp_code')
    phone_number = request.session.get('phone_number')
    address = request.session.get('address')
    city = request.session.get('city')
    state = request.session.get('state')
    zipcode = request.session.get('zipcode')
    customer, _ = Customer.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        submitted_otp = request.POST.get('otp_code')
        if submitted_otp == otp_code:
                # Calculate the total amount of the order.
                total_amount = 0
                # Create PlacedOrder objects for each OrderItem object.
                for order_item in OrderItem.objects.filter(customer=customer):
                    total_amount += order_item.product.price * order_item.quantity
                    placed_order = PlacedOrders.objects.create(
                        order=order_item.order,
                        customer=customer,
                        product=order_item.product,
                        quantity=order_item.quantity,
                        size=order_item.size,
                        address=address,
                        city=city,
                        state=state,
                        zipcode=zipcode,
                        total_amount=total_amount                       
                    )
                placed_order.save()
                del request.session['otp_code']
                del request.session['phone_number']
                del request.session['address']
                del request.session['city']
                del request.session['state']
                del request.session['zipcode']

                # Delete all OrderItem objects for the current user.
                OrderItem.objects.filter(customer=customer).delete()
                return redirect('success')

    return render(request, 'place_order.html')

def placed_orders(request):
  """Displays a list of all placed orders.

  Args:
    request: The HTTP request.

  Returns:
    A rendered template with the list of placed orders.
  """

  placed_orders = PlacedOrders.objects.filter(customer=request.user.customer)

  return render(request, 'placed_orders.html', {
    'placed_orders': placed_orders
  })
def blog(request):
    blogs=Blog.objects.all()
    return render(request,'blog.html',{'posts':blogs})
def blog_detail(request,post_id):
    posts= get_object_or_404(Blog, pk=post_id)
    return render(request,'blog_detail.html',{'blog':posts})