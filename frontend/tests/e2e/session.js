async function startSession(page, username = 'usuario-e2e') {
  await page.addInitScript((sessionUsername) => {
    sessionStorage.setItem('usuario', JSON.stringify({
      username: sessionUsername,
      nombre: 'Usuario de prueba',
      rol: 'user',
    }));
  }, username);
}

module.exports = { startSession };
