document.addEventListener('DOMContentLoaded', function () {
    const burgerMenu = document.querySelector('.burger-menu');
    const navbarPlaceholder = document.querySelector('.navbar_placeholder');

    // Toggle visibility of navbar content on burger menu click
    burgerMenu.addEventListener('click', () => {
        navbarPlaceholder.classList.toggle('navbar-show');
    });
});
