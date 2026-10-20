// Alternância de tema (claro/escuro)
const btnTema = document.getElementById('theme-toggle');
if (btnTema) {
  const raiz = document.documentElement;
  const rotular = (tema) => {
    btnTema.setAttribute('aria-label', tema === 'light' ? 'Ativar modo escuro' : 'Ativar modo claro');
    btnTema.setAttribute('title', tema === 'light' ? 'Modo escuro' : 'Modo claro');
  };
  rotular(raiz.getAttribute('data-theme') || 'dark');

  btnTema.addEventListener('click', () => {
    const novo = raiz.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    raiz.setAttribute('data-theme', novo);
    rotular(novo);
    try { localStorage.setItem('tema', novo); } catch (e) { /* ignora */ }
  });
}

// Ano automático no rodapé
document.getElementById('ano').textContent = new Date().getFullYear();

// Carrossel (só existe na Home)
const track = document.getElementById('track');
if (track) {
  const INTERVALO = 4500; // tempo entre os movimentos, em ms
  const reduzir = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let timer;

  const passo = () => {
    const card = track.querySelector('.card');
    return card.offsetWidth + parseFloat(getComputedStyle(track).columnGap || 16);
  };

  const avancar = () => {
    const fim = track.scrollLeft + track.clientWidth >= track.scrollWidth - 5;
    track.scrollTo({ left: fim ? 0 : track.scrollLeft + passo(), behavior: 'smooth' });
  };
  const voltar = () => {
    const inicio = track.scrollLeft <= 5;
    track.scrollTo({ left: inicio ? track.scrollWidth : track.scrollLeft - passo(), behavior: 'smooth' });
  };

  const iniciar = () => { if (!reduzir) { parar(); timer = setInterval(avancar, INTERVALO); } };
  const parar = () => clearInterval(timer);

  document.getElementById('next').addEventListener('click', () => { avancar(); iniciar(); });
  document.getElementById('prev').addEventListener('click', () => { voltar(); iniciar(); });

  // Pausa quando o usuário interage
  ['mouseenter', 'focusin', 'touchstart'].forEach(e => track.addEventListener(e, parar, { passive: true }));
  ['mouseleave', 'focusout', 'touchend'].forEach(e => track.addEventListener(e, iniciar, { passive: true }));

  iniciar();
}