// ─────────────────────────────────────────────
// SESIÓN
// ─────────────────────────────────────────────

const sesion = JSON.parse(
  sessionStorage.getItem('usuario') || 'null'
);

const usuarioLogin = sesion?.username;


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
let movimientoSeleccionado = null;


// ─────────────────────────────────────────────
// CARGAR AHORRO
// ─────────────────────────────────────────────

async function cargarAhorro() {

  const tbody =
    document.getElementById('tablaBody');

  if (!usuarioLogin) {
    window.location.href = 'login.html';
    return;
  }

  tbody.innerHTML = `
    <tr class="fila-loading">
      <td colspan="3">
        ⏳ Cargando movimientos...
      </td>
    </tr>
  `;

  try {

    const query = new URLSearchParams({ usuario: usuarioLogin });
    const response =
      await fetch(
        `${window.API_BASE}/ahorro?${query}`
      );

    const data =
      await response.json();

    if (
      !response.ok ||
      !data.ok
    ) {

      throw new Error(
        mensajeErrorApi(data, 'Error al cargar el ahorro')
      );

    }

    // Guardamos los movimientos
    movimientos = data.datos;

    // Actualizamos resumen
    renderResumen(data);

    // Actualizamos tabla
    renderTabla(movimientos);

    // Actualizamos fecha
    actualizarTimestamp(data.ultima_actualizacion);

  } catch (error) {

    console.error(error);

    const row = document.createElement('tr');
    row.className = 'fila-vacia';
    const cell = document.createElement('td');
    cell.colSpan = 3;
    cell.textContent = `⚠️ Error al cargar: ${error.message}`;
    row.appendChild(cell);
    tbody.replaceChildren(row);

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

  const liquidez =
    data.liquidez || 0;


  // ─────────────────────────────────────────
  // LIQUIDEZ
  // ─────────────────────────────────────────

  const elementoLiquidez =
    document.getElementById(
      'totalLiquidez'
    );

  elementoLiquidez.textContent =
    fmtEur(liquidez);

  elementoLiquidez.className =
    `card-value ${claseVariacion(liquidez)}`;


  // ─────────────────────────────────────────
  // TOTAL NETO
  // ─────────────────────────────────────────

  const elementoNeto =
    document.getElementById(
      'totalNeto'
    );

  elementoNeto.textContent =
    fmtEur(totalNeto);

  elementoNeto.className =
    `card-value ${claseVariacion(totalNeto)}`;


  const añoActual = new Date().getFullYear();
  const primerAño = añoActual - 3;
  const tarjetasAnuales = Array.from({ length: 4 }, (_, indice) => {
    const año = primerAño + indice;
    const total = Number(totales[año] || 0);
    const totalAnterior = Number(totales[año - 1] || 0);
    const variacion = totalAnterior > 0
      ? ((total - totalAnterior) / totalAnterior) * 100
      : null;

    const tarjeta = document.createElement('article');
    tarjeta.className = 'card';

    const etiqueta = document.createElement('span');
    etiqueta.className = 'card-label';
    etiqueta.textContent = String(año);

    const valor = document.createElement('span');
    valor.className = `card-value ${claseVariacion(total)}`;
    valor.textContent = fmtEur(total);

    const etiquetaVariacion = document.createElement('span');
    etiquetaVariacion.className = `year-variation ${
      variacion === null ? 'neutro' : claseVariacion(variacion)
    }`;
    etiquetaVariacion.textContent = variacion === null
      ? 'Variación: —'
      : `Variación: ${variacion > 0 ? '+' : ''}${fmt.format(variacion)} %`;

    tarjeta.append(etiqueta, valor, etiquetaVariacion);
    return tarjeta;
  });

  document.getElementById('totalesAnuales')
    .replaceChildren(...tarjetasAnuales);

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
    document.getElementById(
      'tablaBody'
    );


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

  const filas = datos.map(movimiento => {
    const esIngreso = movimiento.tipo === 'ingreso';
    const clase = esIngreso ? 'positivo' : 'negativo';
    const signo = esIngreso ? '+' : '-';
    const tipoTexto = esIngreso ? 'Ingreso' : 'Retirada';
    const fila = document.createElement('tr');

    fila.dataset.id = movimiento.id;
    fila.className = 'fila-movimiento';

    const fecha = document.createElement('td');
    fecha.textContent = movimiento.fecha;
    fila.appendChild(fecha);

    const tipo = document.createElement('td');
    const etiquetaTipo = document.createElement('span');
    etiquetaTipo.className = clase;
    etiquetaTipo.textContent = tipoTexto;
    tipo.appendChild(etiquetaTipo);
    fila.appendChild(tipo);

    const importe = document.createElement('td');
    importe.className = `text-right ${clase}`;
    importe.textContent = `${signo}${fmtEur(movimiento.importe)}`;
    fila.appendChild(importe);

    return fila;
  });
  tbody.replaceChildren(...filas);


  // ─────────────────────────────────────────
  // SELECCIÓN DE MOVIMIENTO
  // ─────────────────────────────────────────

  document
    .querySelectorAll('.fila-movimiento')
    .forEach(
      fila => {

        fila.addEventListener(
          'click',
          () => {

            // Deseleccionar todas las filas
            document
              .querySelectorAll(
                '.fila-movimiento'
              )
              .forEach(
                f => {

                  f.classList.remove(
                    'fila-seleccionada'
                  );

                }
              );


            // Seleccionar fila
            fila.classList.add(
              'fila-seleccionada'
            );


            // Guardar ID
            movimientoSeleccionado =
              Number(
                fila.dataset.id
              );


            // Activar botón eliminar
            document.getElementById(
              'btnEliminarMovimiento'
            ).disabled = false;


            console.log(
              'Movimiento seleccionado:',
              movimientoSeleccionado
            );

          }
        );

      }
    );

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
      document.getElementById(
        'buscador'
      );


    buscador.addEventListener(
      'input',
      event => {

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


        renderTabla(
          filtrados
        );

      }
    );


    // ─────────────────────────────────────────
    // REFERENCIAS MODAL MOVIMIENTO
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
    // REFERENCIAS MODAL ELIMINAR
    // ─────────────────────────────────────────

    const btnEliminarMovimiento =
      document.getElementById(
        'btnEliminarMovimiento'
      );


    const modalEliminarMovimiento =
      document.getElementById(
        'modalEliminarMovimiento'
      );


    const btnCerrarModalEliminar =
      document.getElementById(
        'btnCerrarModalEliminar'
      );


    const btnCancelarEliminar =
      document.getElementById(
        'btnCancelarEliminar'
      );


    const btnConfirmarEliminar =
      document.getElementById(
        'btnConfirmarEliminar'
      );


    // ─────────────────────────────────────────
    // REFERENCIAS MODAL LIQUIDEZ
    // ─────────────────────────────────────────

    const btnModificarLiquidez =
      document.getElementById(
        'btnModificarLiquidez'
      );


    const modalLiquidez =
      document.getElementById(
        'modalLiquidez'
      );


    const btnCerrarModalLiquidez =
      document.getElementById(
        'btnCerrarModalLiquidez'
      );


    const btnCancelarLiquidez =
      document.getElementById(
        'btnCancelarLiquidez'
      );


    const liquidezActual =
      document.getElementById(
        'liquidezActual'
      );


    const nuevaLiquidez =
      document.getElementById(
        'nuevaLiquidez'
      );

    const btnGuardarLiquidez =
      document.getElementById(
        'btnGuardarLiquidez'
      );


    const errorLiquidez =
      document.getElementById(
        'errorLiquidez'
      );

    // ─────────────────────────────────────────
    // REFERENCIAS MODAL CONFIRMAR LIQUIDEZ
    // ─────────────────────────────────────────

    const modalConfirmarLiquidez =
      document.getElementById(
        'modalConfirmarLiquidez'
      );

    const btnCerrarModalConfirmarLiquidez =
      document.getElementById(
        'btnCerrarModalConfirmarLiquidez'
      );

    const btnCancelarConfirmarLiquidez =
      document.getElementById(
        'btnCancelarConfirmarLiquidez'
      );

    const btnConfirmarLiquidez =
      document.getElementById(
        'btnConfirmarLiquidez'
      );

    const valorNuevaLiquidez =
      document.getElementById(
        'valorNuevaLiquidez'
      );

    // ─────────────────────────────────────────
    // FUNCIONES MODAL ELIMINAR
    // ─────────────────────────────────────────

    function cerrarModalEliminar() {

      modalEliminarMovimiento
        .classList.remove(
          'modal-visible'
        );

    }


    // ─────────────────────────────────────────
    // FUNCIÓN ABRIR MODAL LIQUIDEZ
    // ─────────────────────────────────────────

    function abrirModalLiquidez() {

      // Mostrar liquidez actual
      liquidezActual.value =
        document.getElementById(
          'totalLiquidez'
        ).textContent;


      // Limpiar nueva cantidad
      nuevaLiquidez.value = '';


      // Limpiar error
      errorLiquidez.textContent = '';


      // Mostrar modal
      modalLiquidez.classList.add(
        'modal-visible'
      );

    }


    // ─────────────────────────────────────────
    // ABRIR MODAL NUEVO MOVIMIENTO
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
    // CERRAR MODAL NUEVO MOVIMIENTO
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
    // CERRAR MODAL ELIMINAR
    // ─────────────────────────────────────────

    btnCerrarModalEliminar.addEventListener(
      'click',
      cerrarModalEliminar
    );


    btnCancelarEliminar.addEventListener(
      'click',
      cerrarModalEliminar
    );


    // ─────────────────────────────────────────
    // ABRIR MODAL ELIMINAR
    // ─────────────────────────────────────────

    btnEliminarMovimiento.addEventListener(
      'click',
      () => {

        if (
          movimientoSeleccionado === null
        ) {
          return;
        }


        modalEliminarMovimiento
          .classList.add(
            'modal-visible'
          );

      }
    );


    // ─────────────────────────────────────────
    // CONFIRMAR ELIMINAR MOVIMIENTO
    // ─────────────────────────────────────────

    btnConfirmarEliminar.addEventListener(
      'click',
      async () => {

        if (
          movimientoSeleccionado === null
        ) {
          return;
        }


        btnConfirmarEliminar.disabled =
          true;


        btnConfirmarEliminar.textContent =
          'Eliminando...';


        try {

          const response =
            await fetch(
              `${window.API_BASE}/ahorro/${movimientoSeleccionado}?${new URLSearchParams({ usuario: usuarioLogin })}`,
              {
                method: 'DELETE'
              }
            );


          const data =
            await response.json();


          if (
            !response.ok ||
            !data.ok
          ) {

            throw new Error(
              mensajeErrorApi(data, 'No se pudo eliminar el movimiento')
            );

          }


          // Limpiar selección
          movimientoSeleccionado =
            null;


          // Cerrar modal
          cerrarModalEliminar();


          // Recargar datos
          await cargarAhorro();


        } catch (error) {

          console.error(error);


          alert(
            `Error al eliminar: ${error.message}`
          );


        } finally {

          btnConfirmarEliminar.disabled =
            false;


          btnConfirmarEliminar.textContent =
            '🗑️ Eliminar';


          btnEliminarMovimiento.disabled =
            true;

        }

      }
    );


    // ─────────────────────────────────────────
    // ABRIR MODAL LIQUIDEZ
    // ─────────────────────────────────────────

    btnModificarLiquidez.addEventListener(
      'click',
      abrirModalLiquidez
    );


    // ─────────────────────────────────────────
    // CERRAR MODAL LIQUIDEZ
    // ─────────────────────────────────────────

    btnCerrarModalLiquidez.addEventListener(
      'click',
      () => {

        modalLiquidez.classList.remove(
          'modal-visible'
        );

      }
    );


    btnCancelarLiquidez.addEventListener(
      'click',
      () => {

        modalLiquidez.classList.remove(
          'modal-visible'
        );

      }
    );


    // ─────────────────────────────────────────
    // GUARDAR NUEVO MOVIMIENTO
    // ─────────────────────────────────────────

    formMovimiento.addEventListener(
      'submit',
      async event => {

        event.preventDefault();


        const tipo =
          document.getElementById(
            'tipoMovimiento'
          ).value;


        const importe =
          parseFloat(
            document.getElementById(
              'importeMovimiento'
            ).value
          );


        const fecha =
          document.getElementById(
            'fechaMovimiento'
          ).value;


        const error =
          document.getElementById(
            'errorMovimiento'
          );


        const boton =
          document.getElementById(
            'btnGuardarMovimiento'
          );


        error.textContent = '';


        // Validar importe
        if (
          !importe ||
          importe <= 0
        ) {

          error.textContent =
            'Introduce un importe válido.';

          return;

        }


        boton.disabled =
          true;


        boton.textContent =
          'Guardando...';


        try {

          const response =
            await fetch(
              `${window.API_BASE}/ahorro`,
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


          if (
            !response.ok ||
            !data.ok
          ) {

            throw new Error(
              mensajeErrorApi(data, 'No se pudo guardar el movimiento')
            );

          }


          // Cerrar modal
          cerrarModal();


          // Recargar datos
          await cargarAhorro();


        } catch (err) {

          console.error(err);


          error.textContent =
            err.message;


        } finally {

          boton.disabled =
            false;


          boton.textContent =
            'Guardar';

        }

      }
    );


    // ─────────────────────────────────────────
    // MODIFICAR LIQUIDEZ
    // ─────────────────────────────────────────

    btnGuardarLiquidez.addEventListener(
      'click',
      () => {

        const importe =
          parseFloat(nuevaLiquidez.value);

        errorLiquidez.textContent = '';

        // Validar importe
        if (
          isNaN(importe) ||
          importe < 0
        ) {

          errorLiquidez.textContent =
            'Introduce una cantidad válida.';

          return;
        }

        // Mostrar la nueva liquidez en el popup
        valorNuevaLiquidez.textContent =
          fmtEur(importe);

        // Guardamos temporalmente el valor
        btnConfirmarLiquidez.dataset.importe =
          importe;

        // Cerramos el modal de edición
        modalLiquidez.classList.remove(
          'modal-visible'
        );

        // Abrimos confirmación
        modalConfirmarLiquidez.classList.add(
          'modal-visible'
        );

      }
    );

    btnCerrarModalConfirmarLiquidez.addEventListener(
      'click',
      () => {

        modalConfirmarLiquidez.classList.remove(
          'modal-visible'
        );

      }
    );


    btnCancelarConfirmarLiquidez.addEventListener(
      'click',
      () => {

        modalConfirmarLiquidez.classList.remove(
          'modal-visible'
        );

      }
    );

    btnConfirmarLiquidez.addEventListener(
      'click',
      async () => {

        const importe =
          parseFloat(
            btnConfirmarLiquidez.dataset.importe
          );

        btnConfirmarLiquidez.disabled = true;

        btnConfirmarLiquidez.textContent =
          'Guardando...';

        try {

          const response =
            await fetch(
              `${window.API_BASE}/liquidez`,
              {
                method: 'PUT',

                headers: {
                  'Content-Type':
                    'application/json'
                },

                body: JSON.stringify({
                  usuario: usuarioLogin,
                  importe: importe,
                  moneda: 'EUR'
                })
              }
            );

          const data =
            await response.json();

          if (
            !response.ok ||
            !data.ok
          ) {

            throw new Error(
              mensajeErrorApi(data, 'No se pudo modificar la liquidez')
            );

          }

          // Cerrar confirmación
          modalConfirmarLiquidez.classList.remove(
            'modal-visible'
          );

          // Limpiar campo
          nuevaLiquidez.value = '';

          // Recargar datos
          await cargarAhorro();

        } catch (error) {

          console.error(error);

          alert(
            `Error al modificar la liquidez: ${error.message}`
          );

        } finally {

          btnConfirmarLiquidez.disabled = false;

          btnConfirmarLiquidez.textContent =
            'Confirmar';

        }

      }
    );


    // ─────────────────────────────────────────
    // CARGAR DATOS INICIALES
    // ─────────────────────────────────────────

    cargarAhorro();

  }
);
