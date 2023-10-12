document.addEventListener("DOMContentLoaded", function () {
    const overlayButtons = document.querySelectorAll(".cbtn");
    let currentIndex = 0;
    let intervalId;

    function changeOpacity() {
      overlayButtons[currentIndex].style.opacity = 0.2; // Reduce opacity for the current button
      currentIndex = (currentIndex + 1) % overlayButtons.length; // Cycle through the buttons
      overlayButtons[currentIndex].style.opacity = 1; // Increase opacity for the next button
    }

    // Start with all buttons faded except the first one
    overlayButtons.forEach(function (button, index) {
      button.style.opacity = index === 0 ? 1 : 0.2;
    });

    // Start the continuous opacity change
    intervalId = setInterval(changeOpacity, 5000); // Change opacity every 5 seconds
  });
