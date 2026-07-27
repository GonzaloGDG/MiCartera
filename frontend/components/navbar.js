/**
 * components/navbar.js
 * ─────────────────────────────────────────────
 * Inyecta la barra de navegación común en todas
 * las pantallas. Marca automáticamente el botón
 * activo según la página actual.
 */

const API_BASE = 'http://localhost:8000/api';

const NAV_ITEMS = [
  { label: '📊 Cartera',              href: 'cartera.html' },
  { label: '💰 Dividendos',           href: 'dividendos.html' },
  { label: '📈 Fundamentales',        href: 'fundamentales.html' },
  { label: '🏦 Ahorro',               href: 'ahorro.html' },
  { label: '📅 Histórico Dividendos', href: 'historico-dividendos.html' },
  { label: '💼 Invertido',            href: 'invertido.html' },
  { label: '🔍 Análisis',             href: 'analisis.html' },
];


function renderNavbar() {

  // Página actual
  const paginaActual = window.location.pathname
    .split('/')
    .pop();

  // Verificar sesión
  const sesion = JSON.parse(
    sessionStorage.getItem('usuario') || 'null'
  );

  if (!sesion) {
    window.location.href = 'login.html';
    return;
  }


  // HTML de la navbar
  const html = `
    <nav class="topbar">

      <div class="topbar-brand">
        <span class="topbar-logo">📈</span>
        <span class="topbar-title">Mi Cartera</span>
      </div>


      <div class="topbar-nav">

        ${NAV_ITEMS.map(item => `
          <a
            href="${item.href}"
            class="nav-btn ${
              paginaActual === item.href
                ? 'nav-btn--active'
                : ''
            }"
          >
            ${item.label}
          </a>
        `).join('')}

      </div>


      <div class="topbar-user">

        <span class="topbar-username">
          👤 ${sesion.nombre}
        </span>

        <button
          class="btn-update"
          id="btnActualizarCotizaciones"
        >
          🔄 Actualizar
        </button>

        <button
          class="btn-logout"
          id="btnLogout"
        >
          Salir
        </button>

      </div>

    </nav>
  `;


  // Inyectar navbar
  document.body.insertAdjacentHTML(
    'afterbegin',
    html
  );


  // ─────────────────────────────────────────────
  // LOGOUT
  // ─────────────────────────────────────────────

  document
    .getElementById('btnLogout')
    .addEventListener('click', () => {

      sessionStorage.removeItem('usuario');
      window.location.href = 'login.html';

    });


  // ─────────────────────────────────────────────
  // ACTUALIZAR COTIZACIONES
  // ─────────────────────────────────────────────

  const btnActualizar = document.getElementById(
    'btnActualizarCotizaciones'
  );

  btnActualizar.addEventListener('click', async () => {

    btnActualizar.disabled = true;
    btnActualizar.textContent = '⏳ Actualizando...';

    try {

      const response = await fetch(
        `${API_BASE}/cotizaciones/actualizar`,
        {
          method: 'POST'
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.mensaje || 'Error al actualizar cotizaciones'
        );
      }

      btnActualizar.textContent = '✅ Actualizado';

      // Si estamos en cartera, recargamos la tabla
      if (typeof refrescarCartera === 'function') {
        await refrescarCartera();
      }

      setTimeout(() => {
        btnActualizar.textContent = '🔄 Actualizar';
      }, 2000);

    } catch (error) {

      console.error(error);

      btnActualizar.textContent = '❌ Error';

      setTimeout(() => {
        btnActualizar.textContent = '🔄 Actualizar';
      }, 3000);

    } finally {

      btnActualizar.disabled = false;

    }

  });

} // ← CIERRE DE renderNavbar()


// ─────────────────────────────────────────────
// EJECUTAR AL CARGAR
// ─────────────────────────────────────────────

document.addEventListener(
  'DOMContentLoaded',
  renderNavbar
);