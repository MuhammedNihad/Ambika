
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
