const { test, expect } = require('@playwright/test');
const { startSession } = require('./session');

test('ahorro refleja un ingreso, muestra años dinámicos y permite borrarlo', async ({ page }) => {
  const movimientos = [];
  let liquidez = 10000;
  let siguienteId = 1;

  await startSession(page);
  await page.route('http://localhost:8000/api/**', async route => {
    const request = route.request();
    const url = new URL(request.url());

    if (url.pathname === '/api/ahorro' && request.method() === 'GET') {
      await route.fulfill({
        json: {
          ok: true,
          datos: [...movimientos],
          total_neto: movimientos.reduce(
            (total, movimiento) =>
              total + (movimiento.tipo === 'ingreso' ? movimiento.importe : -movimiento.importe),
            0
          ),
          totales_anuales: movimientos.reduce((totales, movimiento) => {
            const año = movimiento.fecha.slice(0, 4);
            const importe = movimiento.tipo === 'ingreso'
              ? movimiento.importe
              : -movimiento.importe;
            totales[año] = (totales[año] || 0) + importe;
            return totales;
          }, {}),
          liquidez,
          ultima_actualizacion: '2026-10-01 10:00:00',
        },
      });
      return;
    }

    if (url.pathname === '/api/ahorro' && request.method() === 'POST') {
      const payload = request.postDataJSON();
      const movimiento = { id: siguienteId++, ...payload };
      movimientos.push(movimiento);
      liquidez += payload.tipo === 'ingreso' ? payload.importe : -payload.importe;
      await route.fulfill({
        json: { ok: true, datos: movimiento, liquidez },
      });
      return;
    }

    if (url.pathname === '/api/liquidez' && request.method() === 'PUT') {
      liquidez = request.postDataJSON().importe;
      await route.fulfill({
        json: { ok: true, importe: liquidez, moneda: 'EUR' },
      });
      return;
    }

    const movimientoId = Number(url.pathname.split('/').pop());
    if (url.pathname.startsWith('/api/ahorro/') && request.method() === 'DELETE') {
      const index = movimientos.findIndex(movimiento => movimiento.id === movimientoId);
      if (index < 0) {
        await route.fulfill({ status: 400, json: { detail: 'No se encontró el movimiento' } });
        return;
      }
      const [movimiento] = movimientos.splice(index, 1);
      liquidez += movimiento.tipo === 'ingreso' ? -movimiento.importe : movimiento.importe;
      await route.fulfill({ json: { ok: true, datos: movimiento } });
      return;
    }

    await route.fulfill({ status: 404, json: { detail: 'Ruta no simulada' } });
  });

  await page.goto('/ahorro.html');
  await expect(page.locator('#totalLiquidez')).toHaveText('10.000,00 €');

  await page.getByRole('button', { name: '+ Nuevo movimiento' }).click();
  await page.locator('#tipoMovimiento').selectOption('ingreso');
  await page.locator('#importeMovimiento').fill('250.50');
  await page.locator('#fechaMovimiento').fill('2027-04-10');
  await page.getByRole('button', { name: 'Guardar', exact: true }).click();

  await expect(page.locator('#totalLiquidez')).toHaveText('10.250,50 €');
  await expect(page.locator('#totalNeto')).toHaveText('250,50 €');
  await expect(page.locator('#totalesAnuales .card-label')).toHaveText(['2027']);
  await expect(page.locator('#tablaBody')).toContainText('2027-04-10');
  await expect(page.locator('#lastUpdate')).toContainText('2026');

  await page.getByRole('button', { name: '+ Nuevo movimiento' }).click();
  await page.locator('#tipoMovimiento').selectOption('retirada');
  await page.locator('#importeMovimiento').fill('50');
  await page.locator('#fechaMovimiento').fill('2027-05-10');
  await page.getByRole('button', { name: 'Guardar', exact: true }).click();

  await expect(page.locator('#totalLiquidez')).toHaveText('10.200,50 €');
  await expect(page.locator('#totalNeto')).toHaveText('200,50 €');

  await page.locator('.fila-movimiento').filter({ hasText: 'Retirada' }).click();
  await page.getByRole('button', { name: '🗑️ Eliminar movimiento' }).click();
  await page.getByRole('button', { name: '🗑️ Eliminar', exact: true }).click();

  await expect(page.locator('#totalLiquidez')).toHaveText('10.250,50 €');
  await expect(page.locator('#totalNeto')).toHaveText('250,50 €');

  await page.locator('.fila-movimiento').click();
  await page.getByRole('button', { name: '🗑️ Eliminar movimiento' }).click();
  await page.getByRole('button', { name: '🗑️ Eliminar', exact: true }).click();

  await expect(page.locator('#totalLiquidez')).toHaveText('10.000,00 €');
  await expect(page.locator('#totalNeto')).toHaveText('0,00 €');
  await expect(page.locator('#tablaBody')).toContainText('No hay movimientos registrados');

  await page.getByRole('button', { name: '✏️ Modificar liquidez' }).click();
  await page.locator('#nuevaLiquidez').fill('11000');
  await page.getByRole('button', { name: 'Guardar', exact: true }).click();
  await page.getByRole('button', { name: 'Confirmar', exact: true }).click();

  await expect(page.locator('#totalLiquidez')).toHaveText('11.000,00 €');
});

test('muestra el detalle de error del backend al guardar una retirada rechazada', async ({ page }) => {
  await startSession(page);
  await page.route('http://localhost:8000/api/ahorro**', async route => {
    if (route.request().method() === 'POST') {
      await route.fulfill({
        status: 400,
        json: { detail: 'La retirada supera la liquidez disponible' },
      });
      return;
    }

    await route.fulfill({
      json: {
        ok: true,
        datos: [],
        total_neto: 0,
        totales_anuales: {},
        liquidez: 100,
        ultima_actualizacion: null,
      },
    });
  });

  await page.goto('/ahorro.html');
  await page.getByRole('button', { name: '+ Nuevo movimiento' }).click();
  await page.locator('#tipoMovimiento').selectOption('retirada');
  await page.locator('#importeMovimiento').fill('200');
  await page.locator('#fechaMovimiento').fill('2026-10-10');
  await page.getByRole('button', { name: 'Guardar', exact: true }).click();

  await expect(page.locator('#errorMovimiento'))
    .toHaveText('La retirada supera la liquidez disponible');
});
