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
