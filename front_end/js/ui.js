/* ui.js */

function updateNavButtons() {
  const prevBtn = document.querySelector('.button-prev');
  const nextBtn = document.querySelector('.button-next');

  if (!prevBtn || !nextBtn || typeof swiper === 'undefined') return;

    if (swiper.isBeginning) {
    prevBtn.classList.add('disabled');
  } else {
    prevBtn.classList.remove('disabled');
  }

  if (swiper.isEnd) {
    nextBtn.classList.add('disabled');
  } else {
    nextBtn.classList.remove('disabled');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  updateNavButtons();

  if (typeof swiper !== 'undefined') {
    swiper.on('slideChange', updateNavButtons);
    swiper.on('reachBeginning', updateNavButtons);
    swiper.on('reachEnd', updateNavButtons);
  }
});