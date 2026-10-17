const sesion = JSON.parse(sessionStorage.getItem('usuario') || 'null');
const usuarioLogin = sesion?.username;
const formatoNumero = new Intl.NumberFormat('es-ES', {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

let operaciones = [];
let tickers = {};
let operacionSeleccionada = null;

function formatoMoneda(importe, moneda = 'EUR') {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: moneda,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(importe);
}

function fechaLocalHoy() {
  const hoy = new Date();
  const zonaHoraria = hoy.getTimezoneOffset() * 60000;
  return new Date(hoy.getTime() - zonaHoraria).toISOString().slice(0, 10);
}

function indexarTickers(datos) {
  if (!Array.isArray(datos)) {
    throw new Error('La respuesta de tickers no tiene un formato válido.');
  }
  return Object.fromEntries(datos.map(ticker => [ticker.ticker, ticker]));
}

function titulosDisponibles(ticker) {
  return operaciones.reduce((total, operacion) => {
    if (operacion.ticker !== ticker) return total;
    if (operacion.tipo === 'compra') return total + Number(operacion.titulos);
    if (operacion.tipo === 'venta') return total - Number(operacion.titulos);
    return total;
  }, 0);
}

function actualizarTickersDisponibles() {
  const tipo = document.getElementById('tipoOperacion').value;
  const selector = document.getElementById('tickerOperacion');
  const seleccionAnterior = selector.value;
  const entradas = Object.entries(tickers)
    .filter(([ticker]) => tipo === 'compra' || titulosDisponibles(ticker) > 0)
    .sort(([tickerA], [tickerB]) => tickerA.localeCompare(tickerB));

  selector.replaceChildren();
  entradas.forEach(([ticker, datos]) => {
    const opcion = document.createElement('option');
    opcion.value = ticker;
    opcion.textContent = `${datos.nombre || ticker} (${ticker})`;
    selector.appendChild(opcion);
  });
  if (entradas.some(([ticker]) => ticker === seleccionAnterior)) {
    selector.value = seleccionAnterior;
  }
  actualizarTitulosDividendo();
  actualizarMonedas();
}

function actualizarTitulosDividendo() {
  const tipo = document.getElementById('tipoOperacion').value;
  const ticker = document.getElementById('tickerOperacion').value;
  const campoTitulos = document.getElementById('titulosOperacion');
  const esDividendo = tipo === 'dividendo';
  const eraSoloLectura = campoTitulos.readOnly;

  campoTitulos.readOnly = esDividendo;
  if (esDividendo) {
    campoTitulos.value = titulosDisponibles(ticker);
  } else if (eraSoloLectura) {
    campoTitulos.value = '';
  }

  const campoPrecio = document.getElementById('precioOperacion');
  campoPrecio.min = tipo === 'compra' ? '0' : '0.000001';
}

function actualizarMonedas() {
  const selector = document.getElementById('monedaOperacion');
  const monedaAnterior = selector.value;
  const monedas = new Set(['EUR']);
  Object.values(tickers).forEach(ticker => {
    if (ticker.moneda) monedas.add(ticker.moneda);
  });
  operaciones.forEach(operacion => {
    if (operacion.moneda) monedas.add(operacion.moneda);
  });

  selector.replaceChildren();
  [...monedas].sort().forEach(moneda => {
    const opcion = document.createElement('option');
    opcion.value = moneda;
    opcion.textContent = moneda;
    selector.appendChild(opcion);
  });
  selector.value = monedas.has(monedaAnterior) ? monedaAnterior : 'EUR';
}

function renderResumen(data) {
  document.getElementById('totalInvertido').textContent =
    formatoMoneda(data.total_invertido || 0, data.moneda_resumen || 'EUR');

  const tarjetas = (data.totales_anuales || []).map(anual => {
    const tarjeta = document.createElement('article');
    tarjeta.className = 'card';

    const etiqueta = document.createElement('span');
    etiqueta.className = 'card-label';
    etiqueta.textContent = String(anual.año);

    const valor = document.createElement('span');
    valor.className = 'card-value';
    valor.textContent = formatoMoneda(anual.total, data.moneda_resumen || 'EUR');

    const variacion = document.createElement('span');
    variacion.className = `year-variation ${
      anual.variacion > 0 ? 'positivo' : anual.variacion < 0 ? 'negativo' : 'neutro'
    }`;
    variacion.textContent = anual.variacion === null
      ? 'Variación: —'
      : `Variación: ${anual.variacion > 0 ? '+' : ''}${formatoNumero.format(anual.variacion)} %`;

    tarjeta.append(etiqueta, valor, variacion);
    return tarjeta;
  });
  document.getElementById('totalesAnuales').replaceChildren(...tarjetas);
}

function impactoLiquidez(operacion) {
  const bruto = Number(operacion.titulos) * Number(operacion.precio);
  return operacion.tipo === 'compra'
    ? bruto + Number(operacion.comision)
    : bruto - Number(operacion.comision);
}

function renderTabla(datos) {
  const tbody = document.getElementById('tablaBody');
  operacionSeleccionada = null;
  document.getElementById('btnEliminarOperacion').disabled = true;

  if (!datos.length) {
    const fila = document.createElement('tr');
    fila.className = 'fila-vacia';
    const celda = document.createElement('td');
    celda.colSpan = 7;
    celda.textContent = 'No hay operaciones registradas';
    fila.appendChild(celda);
    tbody.replaceChildren(fila);
    return;
  }

  const filas = datos.map(operacion => {
    const fila = document.createElement('tr');
    fila.className = 'fila-movimiento';
    fila.dataset.id = operacion.id;

    const fecha = document.createElement('td');
    fecha.textContent = operacion.fecha;

    const tipo = document.createElement('td');
    const tipoEtiqueta = document.createElement('span');
    tipoEtiqueta.textContent = {
      compra: 'Compra',
      venta: 'Venta',
      dividendo: 'Dividendo',
    }[operacion.tipo] || operacion.tipo;
    tipoEtiqueta.className = operacion.tipo === 'compra'
      ? 'negativo'
      : operacion.tipo === 'venta' || operacion.tipo === 'dividendo'
        ? 'positivo'
        : 'neutro';
    tipo.appendChild(tipoEtiqueta);

    const empresa = document.createElement('td');
    empresa.className = 'company-cell';
    const nombre = document.createElement('span');
    nombre.className = 'company-name';
    nombre.textContent = tickers[operacion.ticker]?.nombre || operacion.ticker;
    const ticker = document.createElement('span');
    ticker.className = 'badge-ticker';
    ticker.textContent = operacion.ticker;
    empresa.append(nombre, ticker);

    const titulos = document.createElement('td');
    titulos.className = 'text-right';
    titulos.textContent = formatoNumero.format(operacion.titulos);

    const precio = document.createElement('td');
    precio.className = 'text-right';
    precio.textContent = formatoMoneda(operacion.precio, operacion.moneda);

    const comision = document.createElement('td');
    comision.className = 'text-right';
    comision.textContent = formatoMoneda(operacion.comision, operacion.moneda);

    const importe = document.createElement('td');
    const impacto = impactoLiquidez(operacion);
    importe.className = `text-right ${impacto < 0 ? 'negativo' : impacto > 0 ? 'positivo' : 'neutro'}`;
    importe.textContent = `${impacto > 0 ? '+' : ''}${formatoMoneda(impacto, operacion.moneda)}`;

    fila.append(fecha, tipo, empresa, titulos, precio, comision, importe);
    fila.addEventListener('click', () => {
      document.querySelectorAll('.fila-movimiento').forEach(elemento => {
        elemento.classList.remove('fila-seleccionada');
      });
      fila.classList.add('fila-seleccionada');
      operacionSeleccionada = Number(operacion.id);
      document.getElementById('btnEliminarOperacion').disabled = false;
    });
    return fila;
  });
  tbody.replaceChildren(...filas);
}

async function cargarOperaciones() {
  const tbody = document.getElementById('tablaBody');
  tbody.replaceChildren();
  const fila = document.createElement('tr');
  fila.className = 'fila-loading';
  const celda = document.createElement('td');
  celda.colSpan = 7;
  celda.textContent = '⏳ Cargando operaciones...';
  fila.appendChild(celda);
  tbody.appendChild(fila);

  if (!usuarioLogin) {
    window.location.href = 'login.html';
    return;
  }

  try {
    const query = new URLSearchParams({ usuario: usuarioLogin });
    const [respuestaOperaciones, respuestaTickers] = await Promise.all([
      fetch(`${window.API_BASE}/operaciones?${query}`),
      fetch(`${window.API_BASE}/tickers`),
    ]);
    const [datosOperaciones, datosTickers] = await Promise.all([
      respuestaOperaciones.json(),
      respuestaTickers.json(),
    ]);
    if (!respuestaOperaciones.ok || !datosOperaciones.ok) {
      throw new Error(mensajeErrorApi(datosOperaciones, 'Error al cargar las operaciones'));
    }
    if (!respuestaTickers.ok || !datosTickers.ok) {
      throw new Error(mensajeErrorApi(datosTickers, 'Error al cargar los tickers'));
    }
    operaciones = datosOperaciones.datos;
    tickers = indexarTickers(datosTickers.datos);
    renderResumen(datosOperaciones);
    renderTabla(operaciones);
  } catch (error) {
    console.error(error);
    fila.className = 'fila-vacia';
    celda.textContent = `⚠️ Error al cargar: ${error.message}`;
    tbody.replaceChildren(fila);
  }
}

function abrirModal() {
  const formulario = document.getElementById('formOperacion');
  formulario.reset();
  document.getElementById('fechaOperacion').value = fechaLocalHoy();
  document.getElementById('comisionOperacion').value = '0';
  document.getElementById('errorOperacion').textContent = '';
  actualizarTickersDisponibles();
  document.getElementById('modalOperacion').classList.add('modal-visible');
}

document.addEventListener('DOMContentLoaded', () => {
  const tipo = document.getElementById('tipoOperacion');
  const ticker = document.getElementById('tickerOperacion');
  const formulario = document.getElementById('formOperacion');
  const modal = document.getElementById('modalOperacion');

  document.getElementById('btnNuevaOperacion').addEventListener('click', abrirModal);
  document.getElementById('btnCerrarModal').addEventListener('click', () => modal.classList.remove('modal-visible'));
  document.getElementById('btnCancelarOperacion').addEventListener('click', () => modal.classList.remove('modal-visible'));
  tipo.addEventListener('change', actualizarTickersDisponibles);
  ticker.addEventListener('change', () => {
    actualizarTitulosDividendo();
    actualizarMonedas();
  });

  document.getElementById('buscador').addEventListener('input', event => {
    const consulta = event.target.value.trim().toLocaleLowerCase('es');
    const filtradas = operaciones.filter(operacion => {
      const nombre = tickers[operacion.ticker]?.nombre || '';
      return [operacion.fecha, operacion.tipo, operacion.ticker, nombre]
        .some(valor => valor.toLocaleLowerCase('es').includes(consulta));
    });
    renderTabla(filtradas);
  });

  formulario.addEventListener('submit', async event => {
    event.preventDefault();
    const error = document.getElementById('errorOperacion');
    const botonGuardar = document.getElementById('btnGuardarOperacion');
    error.textContent = '';

    const payload = {
      usuario: usuarioLogin,
      tipo: tipo.value,
      ticker: ticker.value,
      fecha: document.getElementById('fechaOperacion').value,
      titulos: Number(document.getElementById('titulosOperacion').value),
      precio: Number(document.getElementById('precioOperacion').value),
      comision: Number(document.getElementById('comisionOperacion').value),
      moneda: document.getElementById('monedaOperacion').value,
      confirmar_precio_cero: false,
    };

    if (payload.tipo === 'compra' && payload.precio === 0) {
      const confirmado = window.confirm(
        'El precio es 0. ¿Confirmas que se trata de un posible dividendo en acciones?'
      );
      if (!confirmado) return;
      payload.confirmar_precio_cero = true;
    }

    botonGuardar.disabled = true;
    try {
      const respuesta = await fetch(`${window.API_BASE}/operaciones`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const datos = await respuesta.json();
      if (!respuesta.ok || !datos.ok) {
        throw new Error(mensajeErrorApi(datos, 'Error al guardar la operación'));
      }
      modal.classList.remove('modal-visible');
      await cargarOperaciones();
    } catch (guardarError) {
      error.textContent = guardarError.message;
    } finally {
      botonGuardar.disabled = false;
    }
  });

  document.getElementById('btnEliminarOperacion').addEventListener('click', async () => {
    if (operacionSeleccionada === null) return;
    if (!window.confirm('¿Seguro que quieres eliminar esta operación? Se revertirá el impacto sobre la liquidez.')) return;

    try {
      const query = new URLSearchParams({ usuario: usuarioLogin });
      const respuesta = await fetch(
        `${window.API_BASE}/operaciones/${operacionSeleccionada}?${query}`,
        { method: 'DELETE' }
      );
      const datos = await respuesta.json();
      if (!respuesta.ok || !datos.ok) {
        throw new Error(mensajeErrorApi(datos, 'Error al eliminar la operación'));
      }
      operacionSeleccionada = null;
      await cargarOperaciones();
    } catch (error) {
      window.alert(error.message);
    }
  });

  cargarOperaciones();
});
