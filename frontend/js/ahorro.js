// const API_BASE = 'http://localhost:8000/api';
// API_BASE ya está declarada en navbar.js


// ─────────────────────────────────────────────
// SESIÓN
// ─────────────────────────────────────────────

const sesion = JSON.parse(
  sessionStorage.getItem('usuario') || 'null'
);

const usuarioLogin = sesion?.username || 'admin';


// ─────────────────────────────────────────────
// FORMATEO
// ─────────────────────────────────────────────

const fmt = new Intl.NumberFormat(
  'es-ES',
  {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }
);

const fmtEur = (valor) => {
  return `${fmt.format(valor)} €`;
};


// ─────────────────────────────────────────────
// ESTADO
// ─────────────────────────────────────────────

let movimientos = [];


// ─────────────────────────────────────────────
// CARGAR AHORRO
// ─────────────────────────────────────────────

async function cargarAhorro() {

  const tbody = document.getElementById('tablaBody');

  tbody.innerHTML = `
    <tr class="fila-loading">
      <td colspan="3">
        ⏳ Cargando movimientos...
      </td>
    </tr>
  `;

  try {

    const response = await fetch(
      `${API_BASE}/ahorro?usuario=${usuarioLogin}`
    );

    const data = await response.json();

    if (!response.ok || !data.ok) {

      throw new Error(
        data.mensaje ||
        'Error al cargar el ahorro'
      );

    }

    // Guardamos los movimientos
    movimientos = data.datos;

    // Actualizamos resumen
    renderResumen(data);

    // Actualizamos tabla
    renderTabla(movimientos);

    // Actualizamos fecha
    document.getElementById(
      'lastUpdate'
    ).textContent =
      `Actualizado: ${new Date().toLocaleString('es-ES')}`;

  } catch (error) {

    console.error(error);

    tbody.innerHTML = `
      <tr class="fila-vacia">
        <td colspan="3">
          ⚠️ Error al cargar: ${error.message}
        </td>
      </tr>
    `;

  }

}


// ─────────────────────────────────────────────
// RESUMEN
// ─────────────────────────────────────────────

function renderResumen(data) {

  const totalNeto =
    data.total_neto || 0;

  const totales =
    data.totales_anuales || {};


  // ─────────────────────────────────────────
  // TOTAL NETO
  // ─────────────────────────────────────────

  const elementoNeto =
    document.getElementById('totalNeto');

  elementoNeto.textContent =
    fmtEur(totalNeto);

  elementoNeto.className =
    `card-value ${claseVariacion(totalNeto)}`;


  // ─────────────────────────────────────────
  // TOTALES ANUALES
  // ─────────────────────────────────────────

  const total2024 =
    totales['2024'] || 0;

  const total2025 =
    totales['2025'] || 0;

  const total2026 =
    totales['2026'] || 0;


  const elemento2024 =
    document.getElementById('total2024');

  const elemento2025 =
    document.getElementById('total2025');

  const elemento2026 =
    document.getElementById('total2026');


  elemento2024.textContent =
    fmtEur(total2024);

  elemento2025.textContent =
    fmtEur(total2025);

  elemento2026.textContent =
    fmtEur(total2026);


  // ─────────────────────────────────────────
  // COLORES
  // ─────────────────────────────────────────

  elemento2024.className =
    `card-value ${claseVariacion(total2024)}`;

  elemento2025.className =
    `card-value ${claseVariacion(total2025)}`;

  elemento2026.className =
    `card-value ${claseVariacion(total2026)}`;

}


// ─────────────────────────────────────────────
// CLASE VARIACIÓN
// ─────────────────────────────────────────────

function claseVariacion(valor) {

  if (valor > 0) {
    return 'positivo';
  }

  if (valor < 0) {
    return 'negativo';
  }

  return 'neutro';

}


// ─────────────────────────────────────────────
// TABLA
// ─────────────────────────────────────────────

function renderTabla(datos) {

  const tbody =
    document.getElementById('tablaBody');


  if (!datos.length) {

    tbody.innerHTML = `
      <tr class="fila-vacia">
        <td colspan="3">
          No hay movimientos registrados
        </td>
      </tr>
    `;

    return;

  }


  tbody.innerHTML =
    datos.map(movimiento => {

      const esIngreso =
        movimiento.tipo === 'ingreso';


      const clase =
        esIngreso
          ? 'positivo'
          : 'negativo';


      const signo =
        esIngreso
          ? '+'
          : '-';


      const tipoTexto =
        esIngreso
          ? 'Ingreso'
          : 'Retirada';


      return `
        <tr>

          <td>
            ${movimiento.fecha}
          </td>

          <td>
            <span class="${clase}">
              ${tipoTexto}
            </span>
          </td>

          <td class="text-right ${clase}">
            ${signo}${fmtEur(movimiento.importe)}
          </td>

        </tr>
      `;

    }).join('');

}


// ─────────────────────────────────────────────
// INICIALIZACIÓN
// ─────────────────────────────────────────────

document.addEventListener(
  'DOMContentLoaded',
  () => {


    // ─────────────────────────────────────────
    // BUSCADOR
    // ─────────────────────────────────────────

    const buscador =
      document.getElementById('buscador');


    buscador.addEventListener(
      'input',
      (event) => {

        const texto =
          event.target.value
            .toLowerCase();


        const filtrados =
          movimientos.filter(
            movimiento =>

              movimiento.fecha
                .toLowerCase()
                .includes(texto)

              ||

              movimiento.tipo
                .toLowerCase()
                .includes(texto)

          );


        renderTabla(filtrados);

      }
    );


    // ─────────────────────────────────────────
    // REFERENCIAS DEL MODAL
    // ─────────────────────────────────────────

    const modalMovimiento =
      document.getElementById(
        'modalMovimiento'
      );


    const btnNuevoMovimiento =
      document.getElementById(
        'btnNuevoMovimiento'
      );


    const btnCerrarModal =
      document.getElementById(
        'btnCerrarModal'
      );


    const btnCancelarMovimiento =
      document.getElementById(
        'btnCancelarMovimiento'
      );


    const formMovimiento =
      document.getElementById(
        'formMovimiento'
      );


    const fechaMovimiento =
      document.getElementById(
        'fechaMovimiento'
      );


    // ─────────────────────────────────────────
    // ABRIR MODAL
    // ─────────────────────────────────────────

    btnNuevoMovimiento.addEventListener(
      'click',
      () => {

        modalMovimiento.classList.add(
          'modal-visible'
        );


        // Fecha actual por defecto
        fechaMovimiento.value =
          new Date()
            .toISOString()
            .split('T')[0];

      }
    );


    // ─────────────────────────────────────────
    // CERRAR MODAL
    // ─────────────────────────────────────────

    function cerrarModal() {

      modalMovimiento.classList.remove(
        'modal-visible'
      );


      formMovimiento.reset();


      document.getElementById(
        'errorMovimiento'
      ).textContent = '';

    }


    btnCerrarModal.addEventListener(
      'click',
      cerrarModal
    );


    btnCancelarMovimiento.addEventListener(
      'click',
      cerrarModal
    );


    // ─────────────────────────────────────────
    // GUARDAR MOVIMIENTO
    // ─────────────────────────────────────────

    formMovimiento.addEventListener(
      'submit',
      async (event) => {

        event.preventDefault();


        // Tipo
        const tipo =
          document.getElementById(
            'tipoMovimiento'
          ).value;


        // Importe
        const importe =
          parseFloat(
            document.getElementById(
              'importeMovimiento'
            ).value
          );


        // Fecha
        const fecha =
          document.getElementById(
            'fechaMovimiento'
          ).value;


        // Elemento error
        const error =
          document.getElementById(
            'errorMovimiento'
          );


        // Botón guardar
        const boton =
          document.getElementById(
            'btnGuardarMovimiento'
          );


        // Limpiamos error anterior
        error.textContent = '';


        // ─────────────────────────────────────
        // VALIDAR IMPORTE
        // ─────────────────────────────────────

        if (!importe || importe <= 0) {

          error.textContent =
            'Introduce un importe válido.';

          return;

        }


        // ─────────────────────────────────────
        // ESTADO BOTÓN
        // ─────────────────────────────────────

        boton.disabled = true;

        boton.textContent =
          'Guardando...';


        try {


          // ───────────────────────────────────
          // POST NUEVO MOVIMIENTO
          // ───────────────────────────────────

          const response =
            await fetch(
              `${API_BASE}/ahorro`,
              {
                method: 'POST',

                headers: {
                  'Content-Type':
                    'application/json'
                },

                body: JSON.stringify({
                  usuario:
                    usuarioLogin,

                  tipo:
                    tipo,

                  importe:
                    importe,

                  fecha:
                    fecha
                })
              }
            );


          const data =
            await response.json();


          // ───────────────────────────────────
          // COMPROBAR RESPUESTA
          // ───────────────────────────────────

          if (
            !response.ok ||
            !data.ok
          ) {

            throw new Error(
              data.mensaje ||
              'No se pudo guardar el movimiento'
            );

          }


          // ───────────────────────────────────
          // CERRAR MODAL
          // ───────────────────────────────────

          cerrarModal();


          // ───────────────────────────────────
          // RECARGAR DATOS
          // ───────────────────────────────────

          await cargarAhorro();


        } catch (err) {

          console.error(err);

          error.textContent =
            err.message;


        } finally {

          boton.disabled = false;

          boton.textContent =
            'Guardar';

        }

      }
    );


    // ─────────────────────────────────────────
    // CARGAR DATOS INICIALES
    // ─────────────────────────────────────────

    cargarAhorro();

  }
);