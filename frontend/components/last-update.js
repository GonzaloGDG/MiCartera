function actualizarTimestamp() {

  const elemento = document.getElementById('lastUpdate');

  if (!elemento) {
    return;
  }

  elemento.textContent =
    `Actualizado: ${new Date().toLocaleString('es-ES')}`;
}