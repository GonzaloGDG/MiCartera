const { test, expect } = require('@playwright/test');
const { startSession } = require('./session');

test('cartera muestra valores de forma segura y la fecha de actualización del backend', async ({ page }) => {
  await startSession(page, 'cuenta-cartera');
  await page.route('http://localhost:8000/api/**', async route => {
    const url = new URL(route.request().url());

    if (url.pathname === '/api/cartera') {
      expect(url.searchParams.get('usuario')).toBe('cuenta-cartera');
      await route.fulfill({
        json: {
          ok: true,
          ultimo_update: '2020-01-02 03:04:05',
          datos: [{
            ticker: 'ANA.MC',
            nombre: '<img id="injected" src=x>',
            num_titulos: 2,
            precio_compra: 100,
            precio_actual: 125,
            variacion_hoy: 2,
            variacion_compra: 25,
            total_invertido: 200,
            total_actual: 250,
            diferencia: 50,
            moneda: 'EUR',
          }],
        },
      });
      return;
    }

    if (url.pathname === '/api/liquidez') {
      await route.fulfill({
        json: { ok: true, total: 500, datos: [], moneda: 'EUR' },
      });
      return;
    }

    await route.fulfill({ status: 404, json: { detail: 'Ruta no simulada' } });
  });

  await page.goto('/cartera.html');
  await expect(page.locator('.nombre-empresa'))
    .toHaveText('<img id="injected" src=x>');
  await expect(page.locator('#injected')).toHaveCount(0);
  await expect(page.locator('#patrimonioTotal')).toHaveText('750,00 €');
  await expect(page.locator('#lastUpdate')).toContainText('2020');
});

test('enlaces de navegación aún no implementados muestran el aviso temporal', async ({ page }) => {
  await startSession(page);
  await page.route('http://localhost:8000/api/**', route =>
    route.fulfill({ status: 404, json: { detail: 'Ruta no simulada' } })
  );

  await page.goto('/dividendos.html');
  await expect(page.getByRole('heading', { name: 'Página no disponible' }))
    .toBeVisible();
  await expect(page.getByText('La página de dividendos todavía no existe.'))
    .toBeVisible();
});
