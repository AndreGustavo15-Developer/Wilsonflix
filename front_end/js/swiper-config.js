/* swiper-config.js */
const API_URL = "http://localhost:5000/api";

const bannerWrapper = document.querySelector('.bannerSwiper .swiper-wrapper');
const thumbsWrapper = document.querySelector('.thumbsSwiper .swiper-wrapper');

let titles = [];
let swiper;
let thumbsSwiper;

async function carregarFilmes() {
  try {
    const res = await fetch(`${API_URL}/popular`);
    const filmes = await res.json();

    bannerWrapper.innerHTML = "";
    thumbsWrapper.innerHTML = "";
    titles = [];

    filmes.forEach(filme => {
      bannerWrapper.innerHTML += `<div class="swiper-slide"><img src="${filme.backdrop}" alt="${filme.title}"></div>`;
      thumbsWrapper.innerHTML += `<div class="swiper-slide"><img src="${filme.poster}" alt="${filme.title}"></div>`;
      titles.push(filme);
    });

    inicializarSwipers();
    carregarDetalhesFilme(titles[0].id);

  } catch (error) {
    console.error("Erro ao carregar filmes:", error);
  }
}

function inicializarSwipers() {
  if (swiper) swiper.destroy();
  if (thumbsSwiper) thumbsSwiper.destroy();

  thumbsSwiper = new Swiper(".thumbsSwiper", {
    spaceBetween: 10,
    slidesPerView: 5,
    breakpoints: {
      200: { slidesPerView: 1.5 },
      400: { slidesPerView: 1.5 },
      600: { slidesPerView: 3 },
      1100: { slidesPerView: 5 }
    },
    freeMode: true,
    watchSlidesProgress: true
  });

  swiper = new Swiper('.bannerSwiper', {
    effect: "fade",
    navigation: { nextEl: '.button-next', prevEl: '.button-prev' },
    pagination: { el: '.swiper-pagination', clickable: true },
    thumbs: { swiper: thumbsSwiper }
  });

  swiper.on('activeIndexChange', () => {
    carregarDetalhesFilme(titles[swiper.activeIndex].id);
  });

  swiper.on('slideChange', updateNavButtons);
  swiper.on('reachBeginning', updateNavButtons);
  swiper.on('reachEnd', updateNavButtons);

  updateNavButtons();
}

// Atualiza UI ao trocar o slide
async function carregarDetalhesFilme(id) {
  try {
    const res = await fetch(`${API_URL}/details/${id}`);
    const filme = await res.json();

    document.querySelector('#title').innerHTML = `<h1>${filme.title}</h1>`;
    document.querySelector('#sub-title').innerHTML = `<p>${filme.genres || filme.categoria}</p>`;
    document.querySelector('#desc').innerHTML = `<p>${filme.overview}</p>`;
    document.querySelector('.rating span').textContent = filme.rating.toFixed(1);

    window.movieTrailerURL = filme.trailer;

    // Botão Trailer ✅
    const btnTrailer = document.querySelector('.btn-trailer');
    if (filme.trailer) {
      btnTrailer.style.display = 'inline-block';
      btnTrailer.onclick = () => {
        window.open(window.movieTrailerURL, "_blank");
      };
    } else {
      btnTrailer.style.display = 'none';
    }

    // Botão Saiba Mais ✅
    const btnSaibaMais = document.querySelector(".btn-primary");
    btnSaibaMais.onclick = () => {
      window.open(`https://www.themoviedb.org/movie/${filme.id}?language=pt-br`, "_blank");
    };

  } catch (error) {
    console.error("Erro ao detalhar filme:", error);
  }
}

async function carregarPorCategoria(type) {
  const endpoint =
    type === "movie" ? "movie" :
    type === "tv" ? "series" :
    type === "kids" ? "kids" :
    "popular";

  try {
    const res = await fetch(`${API_URL}/${endpoint}`);
    const filmes = await res.json();

    if (!filmes || filmes.length === 0) {
      console.error(`Nenhuma mídia retornada para categoria: ${type}`);
      return;
    }

    bannerWrapper.innerHTML = "";
    thumbsWrapper.innerHTML = "";
    titles = filmes;

    filmes.forEach(filme => {
      bannerWrapper.innerHTML += `<div class='swiper-slide'><img src="${filme.backdrop}"></div>`;
      thumbsWrapper.innerHTML += `<div class='swiper-slide'><img src="${filme.poster}"></div>`;
    });

    inicializarSwipers();
    carregarDetalhesFilme(filmes[0].id);

  } catch (err) {
    console.error("Erro ao carregar categoria:", err);
  }
}

document.addEventListener("DOMContentLoaded", carregarFilmes);

document.querySelectorAll(".menu a").forEach(link => {
  link.addEventListener("click", (e) => {
    e.preventDefault();
    const type = link.dataset.type;
    carregarPorCategoria(type);
  });
});
