from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import json
import twilio.rest as twilio
import random
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import RegexValidator
# Create your views here.
from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.http import require_http_methods
from .models import Product,OrderItem,Order,PlacedOrders, AddOn, Blog,Customer,Category,ProductSize,Size
from .forms import ProductForm,PlaceOrderForm,PlacedOrdersForm,ShippingForm,SizeFilterForm
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
    products = Product.objects.all()
    trending_products = Product.objects.order_by('-views')[:10]
    new_arrivals = Product.objects.order_by('-id')[:10]
    categories = Category.objects.all()  # Fetch all categories

    context = {
        'trending_products': trending_products,
        'new_arrivals': new_arrivals,
        'products': products,
        'categories': categories,  # Pass categories to the template
    }
    return render(request, 'all_products.html', context)
def bestseller(request):
    # Fetch all sizes and occasions
    sizes = Size.objects.all()

    # Define occasion choices
    OCCASION_CHOICES = [
        ('Casual Wear', 'Casual Wear'),
        ('Comfort Wear', 'Comfort Wear'),
        ('Street Wear', 'Street Wear'),
        ('Club Wear', 'Club Wear'),
        ('Beach Wear', 'Beach Wear'),
        ('Party Wear', 'Party Wear'),
        ('Holiday Wear', 'Holiday Wear'),
        ('Weekend Wear', 'Weekend Wear'),
        ('College Wear', 'College Wear'),
        ('Office Wear', 'Office Wear'),
    ]
    # Get selected sizes, occasions, and price ranges from the query parameters

    selected_occasions = request.GET.getlist('occasion')
    selected_categories = request.GET.getlist('category')
    selected_price_ranges = request.GET.getlist('price_range')
    search_query = request.GET.get('q', '')
    
    # Perform a search query using the 'search_query' variable

    # Initialize the product queryset
    products = Product.objects.all()
    selected_sort_option = request.GET.get('sort', None)
    selected_categories = request.GET.get('category', '').split(',')
    selected_categories = [int(cat_id) for cat_id in selected_categories if cat_id.isdigit()]
    selected_sizes = request.GET.get('size')
    selected_occasions = request.GET.getlist('occasion') or []
    if selected_sort_option == 'newly_added':
        products = products.order_by('-id')  # Sort by ID (newly added)
    elif selected_sort_option == 'best_seller':
        products = products.order_by('-views')  # Sort by views (best seller)
    elif selected_sort_option == 'price_high_to_low':
        products = products.order_by('-price')  # Sort by price high to low
    elif selected_sort_option == 'price_low_to_high':
        products = products.order_by('price')  # Sort by price low to high
    elif search_query:
        products = Product.objects.filter(name__icontains=search_query)
    # ...

    # Filter products based on selected occasions
    if selected_occasions:
        products = products.filter(occasions__in=selected_occasions).distinct()


    # ...

    # Filter products based on selected sizes
    if selected_sizes:
        products = products.filter(sizes__size__in=selected_sizes).distinct()

    # Filter products based on selected sizes
    # Filter products based on selected categories
    if selected_categories:
        products = products.filter(categories__in=selected_categories).distinct()



    # Filter products based on selected price ranges
    price_filters = {
        'under_999': {'price__lt': 999},
        '999': {'price': 999},
        '999_1499': {'price__gte': 999, 'price__lte': 1499},
        '1499_1999': {'price__gte': 1499, 'price__lte': 1999},
        'above_1999': {'price__gt': 1999},
    }

    for price_range in selected_price_ranges:
        if price_range in price_filters:
            products = products.filter(**price_filters[price_range])

    # Get all categories
    categories = Category.objects.all()
    

    context = {
        'sizes': sizes,
        'selected_sizes': selected_sizes,
        'occasions': OCCASION_CHOICES,
        'selected_occasions': selected_occasions,
        'products': products,
        'categories': categories,
        'selected_categories': selected_categories,
        'selected_price_ranges': selected_price_ranges,
        'search_query': search_query,
    }

    return render(request, 'bestseller.html', context)


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
        selected_product = get_object_or_404(Product, pk=product_id)
        selected_product.views = selected_product.views + 1
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
  	add_ons = AddOn.objects.all()
    if request.user.is_authenticated:
        # User is authenticated, retrieve cart items associated with the user
        user = request.user
        cart, created = Order.objects.get_or_create(customer=user.customer, complete=False)
        order_items = cart.orderitem_set.all()

        # Calculate the price of products and their addon price in the cart
		    total_addon_price_in_cart = sum(sum(addon_item.price for addon_item in order_item.add_on.all()) for order_item in order_items)
		    total_amount = sum(item.product.price * item.quantity for item in order_items)

    		# Add total_addon_price_in_cart to total_amount
		    total_amount += float(total_addon_price_in_cart)
    else:
		    # User is not authenticated, retrieve cart items from the session
		    cart_session = request.session.get('cart', {})
		    order_items = []

		    for product_id, item_data in cart_session.items():
			      product = get_object_or_404(Product, pk=product_id)
			      quantity = item_data.get('quantity', 0)
			      size = item_data.get('size', '')
		      	order_items.append({
				        'id': product.id,
			        	'product': product,
				        'quantity': quantity,
		        		'size': size,
				        'total_price': product.price * quantity,
		       	})

		# Calculate the total addon price in the cart;
		# 'list-of-addons' is only present when addons are added to a product in the cart.
		# If 'list-of-addons' is absent, consider the total addon price as 0.
		# Otherwise, iterate through each item in the cart_session and their respective addons to sum up the prices.
		total_addon_price_in_cart = sum(
			addon['price'] if 'list-of-addons' in item else 0
			for item in cart_session.values()
			for addon in item.get('list-of-addons', []))

		total_amount = sum(item['total_price'] for item in order_items)
		total_amount += float(total_addon_price_in_cart)


    if action == 'increment':
        product_id = request.POST.get('product_id')
        order_item = get_object_or_404(OrderItem, pk=product_id)

        # Increment the quantity by 1
        order_item.quantity += 1
        order_item.save()
        cart_session = request.session.get('cart', {})
        cart_session[product_id] = {'size': size, 'quantity': quantity}
        request.session['cart'] = cart_session

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
        cart_session = request.session.get('cart', {})
        cart_session[product_id] = {'size': size, 'quantity': quantity}
        request.session['cart'] = cart_session

        return JsonResponse({'message': 'Product added to cart successfully.'})

    elif action == 'remove':
        product_id = request.POST.get('product_id')

        # Remove the product from the session cart
        cart_session = request.session.get('cart', {})
        if product_id in cart_session:
            del cart_session[product_id]
            request.session['cart'] = cart_session
            return JsonResponse({'message': 'Product removed from cart successfully.'})

    context = {
        'add_ons': add_ons,
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
        else:
            # If the user is not authenticated, update the session cart
            cart_session = request.session.get('cart', {})
            if item_id in cart_session:
                if new_quantity <= 0:
                    del cart_session[item_id]  # Remove the item if quantity is zero or less
                else:
                    cart_session[item_id]['quantity'] = new_quantity
                request.session['cart'] = cart_session
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

@require_http_methods(["POST"])
def update_addon(request):
	try:
		# Deserialize the JSON data from the request body
		data = json.loads(request.body.decode('utf-8'))
		orderitem_id = data.get('orderitem_id')
		addon_id = data.get('addon_id')

		# Input validation
		if not orderitem_id or not addon_id:
			return JsonResponse({"success": False, "message": "Invalid input data."}, status=400)

		if request.user.is_authenticated:
			order_item = get_object_or_404(OrderItem, pk=orderitem_id)
			customer = order_item.customer

			# Check if the user is associated with the customer object
			if request.user == customer.user:
				# Fetch the OrderItem and with the associated Customer
				addon = get_object_or_404(AddOn, id=addon_id)

				# Check if the addon is already associated with the order_item
				if addon in order_item.add_on.all():
					# Remove the addon from the order_item's ManyToMany relationship
					order_item.add_on.remove(addon)
					return JsonResponse({"success": True, "message": "Addon removed successfully."}, status=200)
				else:
					# Associate the addon with the order_item
					order_item.add_on.add(addon)
					return JsonResponse({"success": True, "message": "Addon associated successfully."}, status=200)
			return JsonResponse({"success": False, "message": "User is not associated with customer object."}, status=403)
		else:
			# For unauthenticated users, the 'orderitem_id' variable should contain the Product ID sent from the frontend,
			# as they intentionally do not have access to the 'OrderItem' model object.
			product_id = orderitem_id
			cart_session = request.session.get('cart', {})
			addon_price = data.get('addon_price')

			if not addon_price:
				return JsonResponse({"success": False, "message": "Invalid price input"}, status=400)

			if str(product_id) not in cart_session.keys():
				return JsonResponse({"success": False, "message": "Given product is not found in cart"}, status=400)
			else:
				if "list-of-addons" not in cart_session[str(product_id)] or cart_session[str(product_id)]['list-of-addons'] == []:
					cart_session[str(product_id)]['list-of-addons'] = [{"addonid": addon_id, "price": addon_price}]
				else:
					addon_list = cart_session[str(product_id)]['list-of-addons']
					value_found = False

					# Iterate through the list and check 'addonid' in each dictionary
					for dictionary in addon_list:
						if 'addonid' in dictionary and dictionary['addonid'] == addon_id:
							value_found = True
							break

					if value_found:
						addon_list.remove({"addonid": addon_id, "price": addon_price})
					else:
						addon_list.append({"addonid": addon_id, "price": addon_price})

				# Save the session to persist the changes
				request.session.save()
				return JsonResponse({"success": True, "message": "Add-on updated for given cart item"}, status=200)
	except Exception as e:
		return JsonResponse({"success": False, "message": "An error occurred while processing the request.", "error": e}, status=500)
  
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