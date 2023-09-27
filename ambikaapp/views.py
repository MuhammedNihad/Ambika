from django.shortcuts import render
from django.http import JsonResponse
import json
# Create your views here.
from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,OrderItem,Order,PlacedOrders
from .forms import ProductForm,PlaceOrderForm
def all_products(request):
	products = Product.objects.all()#get all products
	return render(request, 'all_products.html', {'products': products})
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
		selected_product = Product.objects.get(pk=product_id)
		selected_size = request.GET.get('size')
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
		cart_session = request.session.get('cart', {})
		order_items = []

		for product_id, item_data in cart_session.items():
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
		
		# Check if the user is authenticated
		if request.user.is_authenticated:
			try:
				# Retrieve the OrderItem instance by its ID
				order_item = OrderItem.objects.get(pk=item_id)

				order_item.quantity = new_quantity

				if order_item.quantity <= 0:
					order_item.delete()  # Remove the item if quantity is zero or less
				else:
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
def place_order(request):
    if request.method == 'POST':
        form = PlaceOrderForm(request.POST)
        if form.is_valid():
            # Get the customer for the order (you'll need to implement this logic)
            customer = request.user.customer  # Replace with your customer retrieval logic

            # Create a new PlacedOrder for the customer
            placed_order = PlacedOrders.objects.create(
                customer=customer,
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zipcode=form.cleaned_data['zipcode']
            )

            # Get all the OrderItems for the customer that are not marked as deleted
            order_items = OrderItem.objects.filter(customer=customer, deleted=False)

            # Associate the order items with the placed order using ManyToManyField
            placed_order.order_items.set(order_items)

            # Mark the order items as deleted and update their order reference
            order_items.update(deleted=True, order=placed_order)

            # You can perform any additional actions or validations here

            # Redirect to a success page or return a response
            return render(request, 'cart', {'placed_order': placed_order})

    else:
        form = PlaceOrderForm()

    return render(request, 'place_order.html', {'form': form})
def placed_orders(request):
    placed_orders = PlacedOrders.objects.all()
    return render(request, 'placed_orders.html', {'placed_orders': placed_orders})