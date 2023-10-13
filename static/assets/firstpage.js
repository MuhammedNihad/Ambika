var currentImage = 0; // Index of the current image
        var imageArray = ["https://www.snitch.co.in/cdn/shop/files/4MST2068-04-M14851.jpg?v=1686922552&width=1800", 
        "https://www.snitch.co.in/cdn/shop/files/4MST2068-04-M14888.jpg?v=1686922552&width=1800", 
        "https://www.snitch.co.in/cdn/shop/files/4MST2068-04-M14866.jpg?v=1686922552&width=1800",
        "https://www.snitch.co.in/cdn/shop/files/4MST2068-04-M14848.jpg?v=1686922552&width=1800",
        "https://www.snitch.co.in/cdn/shop/files/4MST2068-04-M14859.jpg?v=1686922552&width=1800",
        "https://www.snitch.co.in/cdn/shop/files/chemical-free-tag-final_d30913d3-12a5-4980-bcc1-5785f1834377.jpg?v=1686922552&width=1800"]; // Array of image URLs



  function changeimage(){
    var image=document.getElementById('image');
    currentImage = (currentImage + 1) % imageArray.length; // Cycle through images
            image.src = imageArray[currentImage];
}

 // JavaScript function to display the clicked image in the container
 function displayImage(imageSrc) {
    var image = document.getElementById('image');
    image.src = imageSrc;
    image.style.display = 'block'; // Show the image
}

function incrementQuantity() {
    var quantityInput = document.getElementById('quantity');
    quantityInput.value = parseInt(quantityInput.value) + 1;
}

function decrementQuantity() {
    var quantityInput = document.getElementById('quantity');
    var currentValue = parseInt(quantityInput.value);
    if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
    }
}


        //------------------- cartpage offcanvas -------------------

        function increment() {
            var quantityInput = document.getElementById('qty');
            quantityInput.value = parseInt(quantityInput.value) + 1;
        }
        
        function decrement() {
            var quantityInput = document.getElementById('qty');
            var currentValue = parseInt(quantityInput.value);
            if (currentValue > 1) {
                quantityInput.value = currentValue - 1;
            }
        }

         // JavaScript to show the offcanvas when the button is clicked
  document.getElementById('showOffcanvas').addEventListener('click', function() {
    var myOffcanvas = new bootstrap.Offcanvas(document.getElementById('myOffcanvas'));
    myOffcanvas.show();
});