// ===== Idioma (Português BR / English) =====
// O português é o idioma padrão e vem escrito no próprio HTML.
// Aqui ficam só as traduções para o inglês (chaves = atributos data-i18n / data-i18n-attr).
const EN = {
  // Comum às duas páginas
  nav_aria: 'Main',
  nav_sobre: 'About the Project',
  foot_desc: 'Academic project that brings together reliable data to raise awareness about the importance of digital security.',
  foot_nav: 'Navigation',
  foot_inicio: 'Home',
  foot_baixar: 'Download guide',
  foot_inst: 'Institution',
  foot_fatec: 'Fatec · Systems Analysis and Development<br>Integrative Project, 1st semester',
  copy: 'CiberPerifa. Non-profit project, made for educational purposes.',

  // Home
  meta_desc: 'Reliable data on cybersecurity and an awareness guide to download.',
  hero_h1: 'Protecting your data starts with understanding the risk.',
  hero_p: 'Today, almost everything we do goes through the internet: banking, work, studies, conversations. Knowing the basics of digital security is the simplest way to avoid scams, leaks and losses.',
  hero_btn: 'Download the guide',
  dados_h2: 'Cybersecurity in numbers',
  dados_lead: 'Data from recognized sources, updated periodically.',
  prev_aria: 'Previous cards',
  next_aria: 'Next cards',
  track_aria: 'Cybersecurity data',
  fonte: 'Source:',
  c1_n: 'US$ 4.44 million',
  c1_p: 'Global average cost of a data breach in 2025.',
  c1_src: 'IBM, 2025 report',
  c2_p: 'of the breaches analyzed involved a human element, such as people\'s actions or mistakes.',
  c3_n: 'US$ 16 billion+',
  c3_p: 'In reported losses from internet crimes in the United States in 2024.',
  c3_src: 'FBI IC3, 2024 report',
  c4_n: 'Brazil data',
  c4_p: 'Browse national statistics on security incidents and fraud attempts.',
  dl_h2: 'Awareness guide',
  dl_p: 'A PDF with detailed data and practical guidance. Each download brings the most recent information we have gathered.',
  dl_btn: 'Download PDF',

  // Sobre o Projeto
  title_sobre: 'CiberPerifa | About the Project',
  s_h1: 'About CiberPerifa',
  s_sub: 'How the idea came about and who we partnered with.',
  s_hist_h2: 'Project history',
  s_hist_p1: 'CiberPerifa was born in the Integrative Project course of the 1st semester of Systems Analysis and Development at Fatec. The challenge was to create a solution tied to a real partner and useful to society. We chose digital security because we want to help people stay informed, with data from reliable sources and in simple language.',
  s_hist_p2: 'The guide\'s data is updated periodically, so that anyone who downloads the file always finds recent information.',
  s_part_h2: 'Our partner',
  s_logo_alt: 'Perifa na Lista logo',
  s_part_p: 'Perifa na Lista is a social project created by Rick Trindade, in the south of Bahia, that seeks to democratize access to culture, leisure and art in Brazilian peripheries, working on a voluntary basis, in partnership with institutions, companies and cultural agents committed to social transformation. The project understands the periphery as a set of historically marginalized experiences, beyond the physical dimension of distance from urban centers. In this sense, Perifa na Lista creates diverse opportunities for connection between the peripheries and different culturally and artistically enriching experiences, promoting well-being, broadening horizons and opening paths so that peripheral communities, collectively, can occupy their rightful place in the Brazilian cultural scene.'
};

// Textos gerados pelo JavaScript (botões de tema e de idioma)
const TXT = {
  pt: {
    temaParaEscuro: 'Ativar modo escuro', temaParaClaro: 'Ativar modo claro',
    tituloEscuro: 'Modo escuro', tituloClaro: 'Modo claro',
    idiomaAria: 'Mudar o idioma para inglês', idiomaTitulo: 'English', idiomaBotao: 'EN'
  },
  en: {
    temaParaEscuro: 'Turn on dark mode', temaParaClaro: 'Turn on light mode',
    tituloEscuro: 'Dark mode', tituloClaro: 'Light mode',
    idiomaAria: 'Switch language to Portuguese', idiomaTitulo: 'Português', idiomaBotao: 'PT'
  }
};

const raiz = document.documentElement;
let idioma = 'pt';
try { if (localStorage.getItem('idioma') === 'en') idioma = 'en'; } catch (e) { /* ignora */ }

// ===== Alternância de tema (claro/escuro) =====
const btnTema = document.getElementById('theme-toggle');
const rotular = (tema) => {
  if (!btnTema) return;
  const t = TXT[idioma];
  btnTema.setAttribute('aria-label', tema === 'light' ? t.temaParaEscuro : t.temaParaClaro);
  btnTema.setAttribute('title', tema === 'light' ? t.tituloEscuro : t.tituloClaro);
};
if (btnTema) {
  rotular(raiz.getAttribute('data-theme') || 'dark');

  btnTema.addEventListener('click', () => {
    const novo = raiz.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    raiz.setAttribute('data-theme', novo);
    rotular(novo);
    try { localStorage.setItem('tema', novo); } catch (e) { /* ignora */ }
  });
}

// ===== Troca de idioma =====
const btnIdioma = document.getElementById('lang-toggle');

function rotularIdioma() {
  if (!btnIdioma) return;
  const t = TXT[idioma];
  btnIdioma.setAttribute('aria-label', t.idiomaAria);
  btnIdioma.setAttribute('title', t.idiomaTitulo);
  btnIdioma.querySelector('span').textContent = t.idiomaBotao;
}

function aplicarIdioma(lang) {
  idioma = lang;
  raiz.setAttribute('lang', lang === 'en' ? 'en' : 'pt-BR');

  // Textos: guarda o original em português na primeira troca e restaura quando voltar
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    if (el.__pt === undefined) el.__pt = el.innerHTML;
    const en = EN[el.dataset.i18n];
    el.innerHTML = (lang === 'en' && en !== undefined) ? en : el.__pt;
  });

  // Atributos (aria-label, alt, content...) no formato "atributo:chave"
  document.querySelectorAll('[data-i18n-attr]').forEach((el) => {
    el.__ptAttr = el.__ptAttr || {};
    el.dataset.i18nAttr.split(',').forEach((par) => {
      const [attr, chave] = par.split(':');
      if (!(attr in el.__ptAttr)) el.__ptAttr[attr] = el.getAttribute(attr);
      const en = EN[chave];
      el.setAttribute(attr, (lang === 'en' && en !== undefined) ? en : el.__ptAttr[attr]);
    });
  });

  rotularIdioma();
  rotular(raiz.getAttribute('data-theme') || 'dark');
}

if (idioma === 'en') {
  aplicarIdioma('en');
} else {
  rotularIdioma();
}

if (btnIdioma) {
  btnIdioma.addEventListener('click', () => {
    const novo = idioma === 'en' ? 'pt' : 'en';
    aplicarIdioma(novo);
    try { localStorage.setItem('idioma', novo); } catch (e) { /* ignora */ }
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