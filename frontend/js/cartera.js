
const API_BASE = 'http://localhost:5000/api';

// ── Sesión (navbar.js ya verifica si no hay sesión) ────
const sesion = JSON.parse(sessionStorage.getItem('usuario') || 'null');
const usuarioLogin = sesion?.username || 'admin';

// ── Formateo ───────────────────────────────────────────
const fmt    = new Intl.NumberFormat('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const fmtEur = (v) => `${fmt.format(v)} €`;
const fmtPct = (v) => `${v > 0 ? '+' : ''}${fmt.format(v)} %`;

function claseVariacion(v) {
  if (v > 0) return 'positivo';
  if (v < 0) return 'negativo';
  return 'neutro';
}

// ── Cargar cartera ─────────────────────────────────────
let datosCartera = [];

async function cargarCartera() {
  const tbody = document.getElementById('tablaBody');
  tbody.innerHTML = '<tr class="fila-loading"><td colspan="10">⏳ Cargando cartera...</td></tr>';

  try {
    const res  = await fetch(`${API_BASE}/cartera?usuario=${usuarioLogin}`);
    const data = await res.json();

    if (!data.ok) throw new Error(data.mensaje);

    datosCartera = data.datos;
    renderTabla(datosCartera);
    renderResumen(datosCartera);
    actualizarTimestamp();

  } catch (err) {
    tbody.innerHTML = `<tr class="fila-vacia"><td colspan="10">⚠️ Error al cargar: ${err.message}</td></tr>`;
  }
}

// ── Renderizar tabla ───────────────────────────────────
function renderTabla(datos) {
  const tbody = document.getElementById('tablaBody');

  if (!datos.length) {
    tbody.innerHTML = '<tr class="fila-vacia"><td colspan="10">No hay posiciones en la cartera</td></tr>';
    return;
  }

  tbody.innerHTML = datos.map(p => {
    const sinDatos     = p.sin_datos;
    const precioActual = sinDatos ? '—' : fmtEur(p.precio_actual);
    const varHoy       = sinDatos ? '—' : `<span class="${claseVariacion(p.variacion_hoy)}">${fmtPct(p.variacion_hoy)}</span>`;
    const varCompra    = sinDatos ? '—' : `<span class="${claseVariacion(p.variacion_compra)}">${fmtPct(p.variacion_compra)}</span>`;
    const totalActual  = sinDatos ? '—' : fmtEur(p.total_actual);
    const diferencia   = sinDatos ? '—' : `<span class="${claseVariacion(p.diferencia)}">${fmtEur(p.diferencia)}</span>`;

    return `
      <tr class="${sinDatos ? 'fila-sin-datos' : ''}">
        <td>
          <div class="nombre-ticker">
            <span class="nombre-empresa">${p.nombre}</span>
          </div>
        </td>
        <td><span class="badge-ticker">${p.ticker}</span></td>
        <td class="text-right">${p.num_titulos}</td>
        <td class="text-right">${fmtEur(p.precio_compra)}</td>
        <td class="text-right">${precioActual}</td>
        <td class="text-right">${varHoy}</td>
        <td class="text-right">${varCompra}</td>
        <td class="text-right">${fmtEur(p.total_invertido)}</td>
        <td class="text-right">${totalActual}</td>
        <td class="text-right">${diferencia}</td>
      </tr>
    `;
  }).join('');
}

// ── Renderizar tarjetas resumen ────────────────────────
function renderResumen(datos) {
  const totalInv = datos.reduce((s, p) => s + p.total_invertido, 0);
  const totalAct = datos.reduce((s, p) => s + (p.total_actual || 0), 0);
  const totalDif = totalAct - totalInv;
  const rentPct  = totalInv ? (totalDif / totalInv * 100) : 0;

  document.getElementById('totalInvertido').textContent = fmtEur(totalInv);
  document.getElementById('totalActual').textContent    = fmtEur(totalAct);

  const elDif  = document.getElementById('totalDiferencia');
  const elRent = document.getElementById('totalRentabilidad');

  elDif.textContent  = fmtEur(totalDif);
  elRent.textContent = fmtPct(rentPct);

  elDif.className  = `card-value ${claseVariacion(totalDif)}`;
  elRent.className = `card-value ${claseVariacion(rentPct)}`;
}

// ── Timestamp ──────────────────────────────────────────
function actualizarTimestamp() {
  const ahora = new Date().toLocaleString('es-ES');
  document.getElementById('lastUpdate').textContent = `Actualizado: ${ahora}`;
}

// ── Buscador ───────────────────────────────────────────
document.getElementById('buscador').addEventListener('input', (e) => {
  const q = e.target.value.toLowerCase();
  const filtrados = datosCartera.filter(p =>
    p.nombre.toLowerCase().includes(q) ||
    p.ticker.toLowerCase().includes(q)
  );
  renderTabla(filtrados);
});

// ── Arranque ───────────────────────────────────────────
cargarCartera();
