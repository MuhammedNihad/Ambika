window.addEventListener('scroll', function () {
    var navbar = document.querySelector('.navbar');
    if (window.scrollY > 0) {
        navbar.classList.add('sticky', 'reveal');
        // Optionally, you can remove the animation class after the animation is complete
        setTimeout(function () {
            navbar.classList.remove('animation');
        }, 500); // Adjust the duration (500ms) to match your animation time
    } else {
        navbar.classList.remove('reveal');
    }
    if (window.scrollY == 0) {
        navbar.classList.remove('reveal');
        setTimeout(function () {
            navbar.classList.remove('sticky');
        }, 400);
    }
})
    // JavaScript to show the offcanvas when the button is clicked
  document.getElementById('showOffcanvas').addEventListener('click', function() {
    var myOffcanvas = new bootstrap.Offcanvas(document.getElementById('myOffcanvas'));
    myOffcanvas.show();
});





