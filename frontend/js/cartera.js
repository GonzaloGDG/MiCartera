
// ── Sesión ─────────────────────────────────────────────
const sesion = JSON.parse(sessionStorage.getItem('usuario') || 'null');
const usuarioLogin = sesion?.username;

// ── Formateo ───────────────────────────────────────────
const fmt = new Intl.NumberFormat('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const fmtEur = (v) => `${fmt.format(v)} €`;
const fmtPct = (v) => `${v > 0 ? '+' : ''}${fmt.format(v)} %`;

function claseVariacion(v) {
  if (v > 0) return 'positivo';
  if (v < 0) return 'negativo';
  return 'neutro';
}

// ── Estado de ordenación + datos ───────────────────────
let datosCartera = [];
let liquidez = 0;
let sortCol = null;
let sortDir = null;

// ── Cargar cartera ─────────────────────────────────────
async function cargarCartera() {

  const tbody = document.getElementById('tablaBody');

  tbody.innerHTML = `
    <tr class="fila-loading">
      <td colspan="10">⏳ Cargando cartera...</td>
    </tr>
  `;

  if (!usuarioLogin) {
    window.location.href = 'login.html';
    return;
  }

  try {
    const query = new URLSearchParams({ usuario: usuarioLogin });

    const [resCartera, resLiquidez] = await Promise.all([
      fetch(`${window.API_BASE}/cartera?${query}`),
      fetch(`${window.API_BASE}/liquidez?${query}`)
    ]);

    const dataCartera = await resCartera.json();
    const dataLiquidez = await resLiquidez.json();

    if (!resCartera.ok || !dataCartera.ok) {
      throw new Error(mensajeErrorApi(dataCartera, 'Error al cargar la cartera'));
    }

    if (!resLiquidez.ok || !dataLiquidez.ok) {
      throw new Error(mensajeErrorApi(dataLiquidez, 'Error al cargar la liquidez'));
    }

    // Guardamos los datos
    datosCartera = dataCartera.datos;

    liquidez = dataLiquidez.total || 0;

    // Renderizamos
    renderTabla(datosCartera);

    renderResumen(datosCartera);

    actualizarTimestamp(dataCartera.ultimo_update);

  } catch (err) {

    console.error(err);

    const row = document.createElement('tr');
    row.className = 'fila-vacia';
    const cell = document.createElement('td');
    cell.colSpan = 10;
    cell.textContent = `⚠️ Error al cargar: ${err.message}`;
    row.appendChild(cell);
    tbody.replaceChildren(row);
  }
}

async function refrescarCartera() {
  await cargarCartera();
}

// ── Ordenación ─────────────────────────────────────────
function siguienteEstado(col) {
  if (sortCol !== col) return 'desc';
  if (sortDir === 'desc') return 'asc';
  return null;
}

function ordenarDatos(datos) {
  if (!sortCol || !sortDir) return [...datos];

  return [...datos].sort((a, b) => {
    let va = a[sortCol];
    let vb = b[sortCol];

    if (typeof va === 'string') {
      va = va.toLowerCase();
      vb = vb.toLowerCase();
      if (va < vb) return sortDir === 'asc' ? -1 : 1;
      if (va > vb) return sortDir === 'asc' ? 1 : -1;
      return 0;
    }
    return sortDir === 'asc' ? va - vb : vb - va;
  });
}

function actualizarCabeceras() {
  document.querySelectorAll('.tabla-cartera th[data-col]').forEach(th => {
    th.querySelector('.sort-icon')?.remove();
    if (th.dataset.col === sortCol && sortDir) {
      const icon = document.createElement('span');
      icon.className = 'sort-icon';
      icon.textContent = sortDir === 'asc' ? ' ▲' : ' ▼';
      th.appendChild(icon);
      th.classList.add('th-activo');
    } else {
      th.classList.remove('th-activo');
    }
  });
}

function inicializarOrdenacion() {
  document.querySelectorAll('.tabla-cartera th[data-col]').forEach(th => {
    th.addEventListener('click', () => {
      sortDir = siguienteEstado(th.dataset.col);
      sortCol = sortDir ? th.dataset.col : null;
      actualizarCabeceras();

      const q = document.getElementById('buscador').value.toLowerCase();
      const filtrados = q
        ? datosCartera.filter(p =>
          (p.nombre || '').toLowerCase().includes(q) ||
          (p.ticker || '').toLowerCase().includes(q))
        : datosCartera;

      renderTabla(ordenarDatos(filtrados));
    });
  });
}

// ── Renderizar tabla ───────────────────────────────────
function renderTabla(datos) {
  const tbody = document.getElementById('tablaBody');

  if (!datos.length) {
    const row = document.createElement('tr');
    row.className = 'fila-vacia';
    const cell = document.createElement('td');
    cell.colSpan = 10;
    cell.textContent = 'No hay posiciones en la cartera';
    row.appendChild(cell);
    tbody.replaceChildren(row);
    return;
  }

  const datosOrdenados = ordenarDatos(datos);
  const filas = datosOrdenados.map(p => {
    const sinDatos = p.sin_datos;
    const precioActual = sinDatos ? '—' : fmtEur(p.precio_actual);
    const totalActual = sinDatos ? '—' : fmtEur(p.total_actual);
    const row = document.createElement('tr');
    if (sinDatos) row.className = 'fila-sin-datos';

    const nombreCell = document.createElement('td');
    const nombre = document.createElement('span');
    nombre.className = 'nombre-empresa';
    nombre.textContent = p.nombre || p.ticker;
    nombreCell.appendChild(nombre);
    row.appendChild(nombreCell);

    const tickerCell = document.createElement('td');
    const ticker = document.createElement('span');
    ticker.className = 'badge-ticker';
    ticker.textContent = p.ticker;
    tickerCell.appendChild(ticker);
    row.appendChild(tickerCell);

    const textValues = [
      p.num_titulos,
      fmtEur(p.precio_compra),
      precioActual,
    ];
    textValues.forEach(value => {
      const cell = document.createElement('td');
      cell.className = 'text-right';
      cell.textContent = value;
      row.appendChild(cell);
    });

    [
      ['variacion_hoy', p.variacion_hoy],
      ['variacion_compra', p.variacion_compra],
    ].forEach(([key, value]) => {
      const cell = document.createElement('td');
      cell.className = 'text-right';
      cell.textContent = sinDatos ? '—' : fmtPct(value);
      if (!sinDatos) cell.classList.add(claseVariacion(value));
      row.appendChild(cell);
    });

    [fmtEur(p.total_invertido), totalActual].forEach(value => {
      const cell = document.createElement('td');
      cell.className = 'text-right';
      cell.textContent = value;
      row.appendChild(cell);
    });

    const differenceCell = document.createElement('td');
    differenceCell.className = 'text-right';
    differenceCell.textContent = sinDatos ? '—' : fmtEur(p.diferencia);
    if (!sinDatos) {
      differenceCell.classList.add(claseVariacion(p.diferencia));
    }
    row.appendChild(differenceCell);
    return row;
  });
  tbody.replaceChildren(...filas);
}

// ── Renderizar tarjetas resumen ────────────────────────
function renderResumen(datos) {

  const totalInv = datos.reduce(
    (s, p) => s + p.total_invertido,
    0
  );

  const totalAct = datos.reduce(
    (s, p) => s + (p.total_actual || 0),
    0
  );

  const totalDif = totalAct - totalInv;

  const rentPct = totalInv
    ? (totalDif / totalInv * 100)
    : 0;

  // Patrimonio total
  const patrimonio = totalAct + liquidez;


  // ─────────────────────────────
  // Tarjetas
  // ─────────────────────────────

  document.getElementById(
    'totalInvertido'
  ).textContent = fmtEur(totalInv);


  document.getElementById(
    'totalActual'
  ).textContent = fmtEur(totalAct);


  document.getElementById(
    'totalLiquidez'
  ).textContent = fmtEur(liquidez);


  document.getElementById(
    'patrimonioTotal'
  ).textContent = fmtEur(patrimonio);


  // ─────────────────────────────
  // Ganancia / pérdida
  // ─────────────────────────────

  const elDif = document.getElementById(
    'totalDiferencia'
  );

  const elRent = document.getElementById(
    'totalRentabilidad'
  );


  elDif.textContent = fmtEur(totalDif);

  elRent.textContent = fmtPct(rentPct);


  elDif.className =
    `card-value ${claseVariacion(totalDif)}`;

  elRent.className =
    `card-value ${claseVariacion(rentPct)}`;
}

// ── Timestamp ──────────────────────────────────────────
// ── Buscador ───────────────────────────────────────────
document.getElementById('buscador').addEventListener('input', (e) => {
  const q = e.target.value.toLowerCase();
  const filtrados = datosCartera.filter(p =>
    (p.nombre || '').toLowerCase().includes(q) ||
    (p.ticker || '').toLowerCase().includes(q)
  );
  renderTabla(filtrados);
});

// ── Arranque ───────────────────────────────────────────
cargarCartera().then(() => inicializarOrdenacion());
