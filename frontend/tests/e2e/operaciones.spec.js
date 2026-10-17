const { test, expect } = require('@playwright/test');
const { startSession } = require('./session');

test('la pantalla de operaciones resume compras y permite registrar una compra gratuita confirmada', async ({ page }) => {
  const añoActual = new Date().getFullYear();
  const operaciones = [{
    id: 1,
    usuario: 'usuario-e2e',
    tipo: 'compra',
    ticker: 'ANA.MC',
    fecha: `${añoActual - 1}-01-01`,
    titulos: 10,
    precio: 100,
    comision: 0,
    moneda: 'EUR',
  }];
  let siguienteId = 2;
  let confirmacionPrecioCero;

  await startSession(page);
  await page.route('http://localhost:8000/api/**', async route => {
    const request = route.request();
    const url = new URL(request.url());

    if (url.pathname === '/api/operaciones' && request.method() === 'GET') {
      await route.fulfill({
        json: {
          ok: true,
          datos: [...operaciones],
          moneda_resumen: 'EUR',
          total_invertido: 1000,
          totales_anuales: Array.from({ length: 6 }, (_, indice) => ({
            año: añoActual - 5 + indice,
            total: indice === 4 ? 1000 : 0,
            variacion: indice === 4 ? 0 : 0,
          })),
        },
      });
      return;
    }

    if (url.pathname === '/api/tickers') {
      await route.fulfill({
        json: {
          ok: true,
          datos: [
            { ticker: 'ANA.MC', nombre: 'Acciona', moneda: 'EUR' },
            { ticker: 'ACX.MC', nombre: 'Acerinox', moneda: 'USD' },
          ],
        },
      });
      return;
    }

    if (url.pathname === '/api/operaciones' && request.method() === 'POST') {
      const payload = request.postDataJSON();
      expect(payload.usuario).toBe('usuario-e2e');
      expect(payload.ticker).toBe('ANA.MC');
      expect(payload.confirmar_precio_cero).toBe(true);
      confirmacionPrecioCero = payload.confirmar_precio_cero;
      operaciones.unshift({ id: siguienteId++, ...payload });
      await route.fulfill({ json: { ok: true, datos: operaciones[0] } });
      return;
    }

    await route.fulfill({ status: 404, json: { detail: 'Ruta no simulada' } });
  });

  await page.goto('/operaciones.html');
  await expect(page.locator('#totalInvertido')).toContainText('1000,00');
  await expect(page.locator('#totalesAnuales .card')).toHaveCount(6);
  await expect(page.locator('#tablaBody')).toContainText('Acciona');

  await page.getByRole('button', { name: '+ Nueva operación' }).click();
  await page.locator('#tipoOperacion').selectOption('compra');
  await page.locator('#tickerOperacion').selectOption('ANA.MC');
  await page.locator('#titulosOperacion').fill('1');
  await page.locator('#precioOperacion').fill('0');
  await page.locator('#comisionOperacion').fill('0');
  page.once('dialog', dialog => dialog.accept());
  await page.getByRole('button', { name: 'Guardar', exact: true }).click();

  await expect.poll(() => confirmacionPrecioCero).toBe(true);
  await expect(page.locator('#tablaBody tr')).toHaveCount(2);
});

test('al registrar un dividendo se fijan los títulos disponibles de la posición', async ({ page }) => {
  const operaciones = [{
    id: 1,
    usuario: 'usuario-e2e',
    tipo: 'compra',
    ticker: 'ANA.MC',
    fecha: '2025-01-01',
    titulos: 12,
    precio: 10,
    comision: 0,
    moneda: 'EUR',
  }];

  await startSession(page);
  await page.route('http://localhost:8000/api/**', async route => {
    const request = route.request();
    const url = new URL(request.url());
    if (url.pathname === '/api/operaciones' && request.method() === 'GET') {
      await route.fulfill({
        json: {
          ok: true,
          datos: [...operaciones],
          moneda_resumen: 'EUR',
          total_invertido: 120,
          totales_anuales: [],
        },
      });
      return;
    }
    if (url.pathname === '/api/tickers') {
      await route.fulfill({
        json: {
          ok: true,
          datos: [
            { ticker: 'ANA.MC', nombre: 'Acciona', moneda: 'EUR' },
            { ticker: 'ACX.MC', nombre: 'Acerinox', moneda: 'USD' },
          ],
        },
      });
      return;
    }
    if (url.pathname === '/api/operaciones' && request.method() === 'POST') {
      const payload = request.postDataJSON();
      expect(payload.tipo).toBe('dividendo');
      expect(payload.ticker).toBe('ANA.MC');
      expect(payload.titulos).toBe(12);
      await route.fulfill({ json: { ok: true, datos: { id: 2, ...payload } } });
      return;
    }
    await route.fulfill({ status: 404, json: { detail: 'Ruta no simulada' } });
  });

  await page.goto('/operaciones.html');
  await page.getByRole('button', { name: '+ Nueva operación' }).click();
  await page.locator('#tipoOperacion').selectOption('dividendo');
  await expect(page.locator('#tickerOperacion option')).toHaveCount(1);
  await expect(page.locator('#tickerOperacion')).toHaveValue('ANA.MC');
  await expect(page.locator('#titulosOperacion')).toHaveValue('12');
  await expect(page.locator('#titulosOperacion')).toHaveAttribute('readonly', '');
  await page.locator('#precioOperacion').fill('0.5');
  await page.getByRole('button', { name: 'Guardar', exact: true }).click();
});

test('la venta limita los tickers a posiciones y permite borrar la última operación', async ({ page }) => {
  const operaciones = [{
    id: 1,
    usuario: 'usuario-e2e',
    tipo: 'compra',
    ticker: 'ANA.MC',
    fecha: '2025-01-01',
    titulos: 10,
    precio: 100,
    comision: 0,
    moneda: 'EUR',
  }];
  let ventaRegistrada;
  let borradoSolicitado;

  await startSession(page);
  await page.route('http://localhost:8000/api/**', async route => {
    const request = route.request();
    const url = new URL(request.url());

    if (url.pathname === '/api/operaciones' && request.method() === 'GET') {
      await route.fulfill({
        json: {
          ok: true,
          datos: [...operaciones],
          moneda_resumen: 'EUR',
          total_invertido: 1000,
          totales_anuales: [],
        },
      });
      return;
    }

    if (url.pathname === '/api/tickers') {
      await route.fulfill({
        json: {
          ok: true,
          datos: [
            { ticker: 'ANA.MC', nombre: 'Acciona', moneda: 'EUR' },
            { ticker: 'ACX.MC', nombre: 'Acerinox', moneda: 'EUR' },
          ],
        },
      });
      return;
    }

    if (url.pathname === '/api/operaciones' && request.method() === 'POST') {
      const payload = request.postDataJSON();
      expect(payload.usuario).toBe('usuario-e2e');
      expect(payload.tipo).toBe('venta');
      expect(payload.ticker).toBe('ANA.MC');
      expect(payload.titulos).toBe(2);
      ventaRegistrada = { id: 2, ...payload };
      operaciones.unshift(ventaRegistrada);
      await route.fulfill({ json: { ok: true, datos: ventaRegistrada } });
      return;
    }

    if (url.pathname === '/api/operaciones/2' && request.method() === 'DELETE') {
      expect(url.searchParams.get('usuario')).toBe('usuario-e2e');
      borradoSolicitado = true;
      operaciones.splice(operaciones.findIndex(operacion => operacion.id === 2), 1);
      await route.fulfill({ json: { ok: true, datos: ventaRegistrada } });
      return;
    }

    await route.fulfill({ status: 404, json: { detail: 'Ruta no simulada' } });
  });

  await page.goto('/operaciones.html');
  await page.getByRole('button', { name: '+ Nueva operación' }).click();
  await page.locator('#tipoOperacion').selectOption('venta');
  await expect(page.locator('#tickerOperacion option')).toHaveCount(1);
  await expect(page.locator('#tickerOperacion')).toHaveValue('ANA.MC');
  await page.locator('#titulosOperacion').fill('2');
  await page.locator('#precioOperacion').fill('110');
  await page.getByRole('button', { name: 'Guardar', exact: true }).click();

  await expect.poll(() => ventaRegistrada).toBeTruthy();
  await expect(page.locator('#tablaBody tr')).toHaveCount(2);
  await page.locator('#tablaBody tr[data-id="2"]').click();
  await page.once('dialog', dialog => dialog.accept());
  await page.getByRole('button', { name: '🗑️ Eliminar operación' }).click();

  await expect.poll(() => borradoSolicitado).toBe(true);
  await expect(page.locator('#tablaBody tr')).toHaveCount(1);
  await expect(page.locator('#tablaBody')).not.toContainText('Venta');
});
