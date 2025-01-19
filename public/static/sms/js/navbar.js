// JavaScript to set the 'active' class based on the current page URL
document.addEventListener("DOMContentLoaded", function() {
    const currentPage = window.location.pathname; // Get the current page path
    const navLinks = {
        "/": "home-link",
        "/about/": "about-link",
        "/contact/": "contact-link",
        "/admission/": "admission-link"
    };

    // Remove 'active' class from all links first
    document.querySelectorAll(".nav_link").forEach(link => {
        link.classList.remove("active");
    });

    // Add 'active' class to the matching link if it exists in the navLinks object
    if (navLinks[currentPage]) {
        document.getElementById(navLinks[currentPage]).classList.add("active");
    }

    console.log(currentPage);
});
