/* menu.js */
const hamburger = document.getElementById("hamburger");
const mainNav = document.querySelector(".main-nav");
const iconMenu = document.getElementById("icon-menu");

if (hamburger && mainNav) {
  hamburger.addEventListener("click", () => {
    mainNav.classList.toggle("active");
    if (iconMenu) {
      iconMenu.classList.toggle("fa-bars");
      iconMenu.classList.toggle("fa-times");
    }

    if (mainNav.classList.contains('active')) {
      const mobileInput = document.querySelector('.main-nav .mobile-search input');
      if (mobileInput) mobileInput.focus();
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  });

  document.addEventListener('click', (e) => {
    if (!mainNav.classList.contains('active')) return;
    const isClickInside = mainNav.contains(e.target) || hamburger.contains(e.target);
    if (!isClickInside) {
      mainNav.classList.remove('active');
      if (iconMenu) {
        iconMenu.classList.add('fa-bars');
        iconMenu.classList.remove('fa-times');
      }
      document.body.style.overflow = '';
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('.menu a').forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      const type = event.target.getAttribute('data-type');
      carregarPorCategoria(type);
    });
  });
});
