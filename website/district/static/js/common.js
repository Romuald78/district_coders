document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menuToggle');
    const mobileMenu = document.getElementById('mobileMenu');

    menuToggle.addEventListener('click', () => {
    if (mobileMenu.classList.contains('hidden')) {
      mobileMenu.classList.remove('hidden');
      mobileMenu.classList.add('animate__animated', 'animate__slideInDown');
    } else {
      mobileMenu.classList.add('hidden');
      mobileMenu.classList.remove('animate__animated', 'animate__slideInDown');
    }
    });
});

