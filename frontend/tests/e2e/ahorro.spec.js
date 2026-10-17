const { test, expect } = require('@playwright/test');
const { startSession } = require('./session');

test('ahorro refleja un ingreso, muestra años dinámicos y permite borrarlo', async ({ page }) => {
  const añoActual = new Date().getFullYear();
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
          }, Object.fromEntries(
            Array.from({ length: 5 }, (_, indice) => [String(añoActual - 4 + indice), 0])
          )),
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
  await page.locator('#fechaMovimiento').fill(`${añoActual}-04-10`);
  await page.getByRole('button', { name: 'Guardar', exact: true }).click();

  await expect(page.locator('#totalLiquidez')).toHaveText('10.250,50 €');
  await expect(page.locator('#totalNeto')).toHaveText('250,50 €');
  await expect(page.locator('#totalesAnuales .card')).toHaveCount(4);
  await expect(page.locator('#totalesAnuales .card-label')).toHaveText(
    Array.from({ length: 4 }, (_, indice) => String(añoActual - 3 + indice))
  );
  await expect(page.locator('#totalesAnuales .year-variation')).toHaveText([
    'Variación: —',
    'Variación: —',
    'Variación: —',
    'Variación: —',
  ]);
  await expect(page.locator('#tablaBody')).toContainText(`${añoActual}-04-10`);
  await expect(page.locator('#lastUpdate')).toContainText('2026');

  await page.getByRole('button', { name: '+ Nuevo movimiento' }).click();
  await page.locator('#tipoMovimiento').selectOption('retirada');
  await page.locator('#importeMovimiento').fill('50');
  await page.locator('#fechaMovimiento').fill(`${añoActual}-05-10`);
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

test('el resumen anual calcula el porcentaje y distribuye cuatro tarjetas en dos columnas', async ({ page }) => {
  const añoActual = new Date().getFullYear();
  const totales = {
    [añoActual - 4]: -100,
    [añoActual - 3]: 1000,
    [añoActual - 2]: 0,
    [añoActual - 1]: 1000,
    [añoActual]: 1500,
  };

  await startSession(page);
  await page.route('http://localhost:8000/api/ahorro**', async route => {
    await route.fulfill({
      json: {
        ok: true,
        datos: [],
        total_neto: 3500,
        totales_anuales: totales,
        liquidez: 10000,
        ultima_actualizacion: null,
      },
    });
  });

  await page.goto('/ahorro.html');

  const tarjetas = page.locator('#totalesAnuales .card');
  await expect(tarjetas).toHaveCount(4);
  await expect(page.locator('#totalesAnuales .card-label')).toHaveText(
    Array.from({ length: 4 }, (_, indice) => String(añoActual - 3 + indice))
  );
  await expect(tarjetas.nth(0).locator('.card-value')).toHaveText('1000,00 €');
  await expect(tarjetas.nth(0).locator('.year-variation')).toHaveText('Variación: —');
  await expect(tarjetas.nth(1).locator('.card-value')).toHaveText('0,00 €');
  await expect(tarjetas.nth(1).locator('.year-variation')).toHaveText(
    'Variación: -100,00 %'
  );
  await expect(tarjetas.nth(2).locator('.year-variation')).toHaveText('Variación: —');
  await expect(tarjetas.nth(3).locator('.card-value')).toHaveText('1500,00 €');
  await expect(tarjetas.nth(3).locator('.year-variation')).toHaveText(
    'Variación: +50,00 %'
  );

  const columnas = await page.locator('#totalesAnuales').evaluate(element =>
    getComputedStyle(element).gridTemplateColumns.split(' ').length
  );
  expect(columnas).toBe(2);

  await page.setViewportSize({ width: 390, height: 844 });
  const columnasMovil = await page.locator('#totalesAnuales').evaluate(element =>
    getComputedStyle(element).gridTemplateColumns.split(' ').length
  );
  expect(columnasMovil).toBe(1);
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
