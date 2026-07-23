
/**
 * components/navbar.js
 * ─────────────────────────────────────────────
 * Inyecta la barra de navegación común en todas
 * las pantallas. Marca automáticamente el botón
 * activo según la página actual.
 */

const NAV_ITEMS = [
  { label: '📊 Cartera',             href: 'cartera.html' },
  { label: '💰 Dividendos',          href: 'dividendos.html' },
  { label: '📈 Fundamentales',       href: 'fundamentales.html' },
  { label: '🏦 Ahorro',              href: 'ahorro.html' },
  { label: '📅 Histórico Dividendos',href: 'historico-dividendos.html' },
  { label: '💼 Invertido',           href: 'invertido.html' },
  { label: '🔍 Análisis',            href: 'analisis.html' },
];

function renderNavbar() {
  // Página actual
  const paginaActual = window.location.pathname.split('/').pop();

  // Verificar sesión
  const sesion = JSON.parse(sessionStorage.getItem('usuario') || 'null');
  if (!sesion) {
    window.location.href = 'login.html';
    return;
  }

  const html = `
    <nav class="topbar">
      <div class="topbar-brand">
        <span class="topbar-logo">📈</span>
        <span class="topbar-title">CarteraApp</span>
      </div>

      <div class="topbar-nav">
        ${NAV_ITEMS.map(item => `
          <a href="${item.href}"
             class="nav-btn ${paginaActual === item.href ? 'nav-btn--active' : ''}">
            ${item.label}
          </a>
        `).join('')}
      </div>

      <div class="topbar-user">
        <span class="topbar-username">👤 ${sesion.nombre}</span>
        <button class="btn-logout" id="btnLogout">Salir</button>
      </div>
    </nav>
  `;

  // Inyectar en el body
  document.body.insertAdjacentHTML('afterbegin', html);

  // Logout
  document.getElementById('btnLogout').addEventListener('click', () => {
    sessionStorage.removeItem('usuario');
    window.location.href = 'login.html';
  });
}

// Ejecutar al cargar
document.addEventListener('DOMContentLoaded', renderNavbar);
