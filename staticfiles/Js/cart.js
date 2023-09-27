console.log("hello world")
    // Add click event listeners to size buttons
    const sizeButtons = document.querySelectorAll('.size-btn');
    sizeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.getAttribute('data-product');
            const size = button.getAttribute('data-size');
            
            // Now you can use 'productId' and 'size' in your logic
            console.log(`Product ID: ${productId}, Size: ${size}`);
        });
    });
    document.addEventListener('DOMContentLoaded', function () {
        // Get references to the size buttons, selected size element, and quantity elements
        const sizeButtons = document.querySelectorAll('.size-button');
        const selectedSize = document.getElementById('selected-size');
        const decreaseQuantity = document.getElementById('decrease-quantity');
        const increaseQuantity = document.getElementById('increase-quantity');
        const quantityElement = document.getElementById('quantity');
        
        // Initialize cart quantity to 1
        let quantity = 1;
    
        // Add a click event listener to each size button
        sizeButtons.forEach(button => {
            button.addEventListener('click', function () {
                // Get the size value from the data-size attribute of the clicked button
                const size = this.getAttribute('data-size');
                // Update the displayed size
                selectedSize.textContent = size;
            });
        });
    
        // Decrease quantity
        decreaseQuantity.addEventListener('click', function () {
            if (quantity > 1) {
                quantity--;
                quantityElement.textContent = quantity;
            }
        });
    
        // Increase quantity
        increaseQuantity.addEventListener('click', function () {
            quantity++;
            quantityElement.textContent = quantity;
        });
    
        // Add a click event listener to the "Add" button
        const addButton = document.getElementById('add-button');
        addButton.addEventListener('click', function () {
            // Get the product ID and selected size
            const productID = this.getAttribute('data-product');
            const size = selectedSize.textContent;
    
            // Create a data object to send in the request
            const data = {
                'product_id': productID,
                'action': 'addButton',
                'size': size,
                'quantity': quantity  // Include the selected quantity
            };
     function getToken(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        const csrftoken = getToken('csrftoken'); 
            // Send the AJAX request to add the product to the cart
            fetch('/add_to_cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === 'Product added to cart successfully') {
                    // Reset quantity to 1 after adding to cart
                    quantity = 1;
                    quantityElement.textContent = quantity;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Handle error (e.g., display an error message to the user)
            });
        });
    });