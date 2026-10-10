const { test, expect } = require('@playwright/test');

test('login guarda el usuario autenticado y consulta la cartera de esa cuenta', async ({ page }) => {
  const usuariosConsultados = [];

  await page.route('http://localhost:8000/api/**', async route => {
    const url = new URL(route.request().url());

    if (url.pathname === '/api/login') {
      const payload = route.request().postDataJSON();
      await route.fulfill({
        json: payload.username === 'cuenta-personal' && payload.password === 'clave'
          ? {
              ok: true,
              username: payload.username,
              nombre: 'Cuenta personal',
              rol: 'user',
            }
          : { ok: false, mensaje: 'Usuario o contraseña incorrectos' },
      });
      return;
    }

    if (url.pathname === '/api/cartera') {
      usuariosConsultados.push(url.searchParams.get('usuario'));
      await route.fulfill({
        json: { ok: true, datos: [], ultimo_update: null },
      });
      return;
    }

    if (url.pathname === '/api/liquidez') {
      await route.fulfill({
        json: { ok: true, total: 1250, datos: [], moneda: 'EUR' },
      });
      return;
    }

    await route.fulfill({ status: 404, json: { detail: 'Ruta no simulada' } });
  });

  await page.goto('/login.html');
  await page.getByLabel('Usuario').fill('cuenta-personal');
  await page.getByLabel('Contraseña').fill('clave');
  await page.getByRole('button', { name: 'Entrar' }).click();

  await expect(page).toHaveURL(/cartera\.html$/);
  await expect.poll(() => usuariosConsultados).toContain('cuenta-personal');
  await expect(page.locator('.topbar-username')).toContainText('Cuenta personal');

  const sesion = await page.evaluate(() =>
    JSON.parse(sessionStorage.getItem('usuario'))
  );
  expect(sesion.username).toBe('cuenta-personal');
});

test('login muestra el mensaje devuelto por la API para credenciales incorrectas', async ({ page }) => {
  await page.route('http://localhost:8000/api/login', route =>
    route.fulfill({
      json: { ok: false, mensaje: 'Usuario o contraseña incorrectos' },
    })
  );

  await page.goto('/login.html');
  await page.getByLabel('Usuario').fill('usuario-equivocado');
  await page.getByLabel('Contraseña').fill('clave');
  await page.getByRole('button', { name: 'Entrar' }).click();

  await expect(page.locator('#loginError'))
    .toHaveText('Usuario o contraseña incorrectos');
  await expect(page).toHaveURL(/login\.html$/);
});

test('ahorro redirige al login si no hay sesión', async ({ page }) => {
  await page.goto('/ahorro.html');
  await expect(page).toHaveURL(/login\.html$/);
});
