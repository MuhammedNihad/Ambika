
        // top button 
        
     // Get a reference to the button element
     const scrollToTopBtn = document.getElementById("scrollToTopBtn");

     // Add a click event listener to scroll to the top when clicked
     scrollToTopBtn.addEventListener("click", () => {
         // Scroll to the top of the document with smooth behavior
         window.scrollTo({
             top: 0,
             behavior: "smooth"
         });
     });

     // Show the button when the user scrolls down 20px from the top of the document
     window.addEventListener("scroll", () => {
         if (document.documentElement.scrollTop > 20) {
             scrollToTopBtn.style.display = "block";
         } else {
             scrollToTopBtn.style.display = "none";
         }
     });