function actualizarTimestamp(ultimaActualizacion) {

  const elemento = document.getElementById('lastUpdate');

  if (!elemento) {
    return;
  }

  if (!ultimaActualizacion) {
    elemento.textContent = 'Actualización de datos no disponible';
    return;
  }

  const fecha = new Date(
    ultimaActualizacion.replace(' ', 'T')
  );

  elemento.textContent = Number.isNaN(fecha.getTime())
    ? 'Actualización de datos no disponible'
    : `Datos actualizados: ${fecha.toLocaleString('es-ES')}`;
}