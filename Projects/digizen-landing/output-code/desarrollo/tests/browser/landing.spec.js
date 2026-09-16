import { test, expect } from '@playwright/test';

test('responsive topology, no horizontal overflow, screenshots', async ({ page }) => {
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  for (const width of [375, 767, 768, 1023, 1024, 1440]) {
    await page.setViewportSize({ width, height: 960 });
    await page.goto('/');
    await expect(page.locator('main > section')).toHaveCount(16);
    await expect(page.locator('.pricing-card')).toHaveCount(3);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    const nav = await page.locator('.dg-nav').boundingBox();
    expect(nav.width).toBeLessThan(width);
    if (width < 1024) {
      for (const block of ['beat-1', 'beat-2', 'beat-4']) {
        const figure = page.locator(`[data-block="${block}"] figure`).first();
        const box = await figure.boundingBox();
        expect(Math.abs(box.width / box.height - 16 / 9)).toBeLessThan(.02);
        const heading = await page.locator(`[data-block="${block}"] h2`).boundingBox();
        expect(box.y).toBeLessThan(heading.y);
      }
    }
    if (width === 375 || width === 1440) {
      await page.screenshot({ path: `test-results/hero-${width}.png` });
      await page.locator('[data-block="safety"]').screenshot({ path: `test-results/safety-${width}.png` });
      await page.locator('[data-block="payment-options"]').screenshot({ path: `test-results/pricing-${width}.png` });
    }
  }
  expect(errors).toEqual([]);
});

test('form validates, keeps channels independent, never sends in preview', async ({ page }) => {
  const posts = [];
  page.on('request', request => { if (request.method() === 'POST') posts.push(request.url()); });
  await page.goto('/');
  const form = page.locator('main [data-ada-form]');
  await form.locator('[type="submit"]').click();
  await expect(form.locator('[name="parent_name"]')).toHaveAttribute('aria-invalid', 'true');
  await form.locator('[name="parent_name"]').fill('Ana López');
  await form.locator('[name="contact"]').fill('ana@example.com');
  await form.locator('[value="whatsapp"]').check();
  await expect(form.locator('[name="contact"]')).toHaveValue('');
  await form.locator('[name="contact"]').fill('+52 55 1234 5678');
  await form.locator('[value="email"]').check();
  await expect(form.locator('[name="contact"]')).toHaveValue('ana@example.com');
  await form.locator('[type="submit"]').click();
  await expect(form.locator('.form-status')).toContainText('no se enviaron');
  expect(posts).toEqual([]);
});

test('ADA modal traps focus, closes with Escape and returns to its trigger', async ({ page }) => {
  await page.goto('/');
  const trigger = page.locator('[data-action="ada"]').first();
  await trigger.click();
  await expect(page.locator('#ada-dialog')).toBeVisible();
  await expect(page.locator('#ada-dialog [name="parent_name"]')).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(page.locator('#ada-dialog')).not.toBeVisible();
  await expect(trigger).toBeFocused();
  const ids = await page.locator('[id]').evaluateAll(nodes => nodes.map(node => node.id));
  expect(new Set(ids).size).toBe(ids.length);
});

test('pricing keeps plan intent and an honest preview', async ({ page }) => {
  await page.goto('/');
  await page.locator('.pricing-card [data-plan="monthly"]').click();
  await expect(page.locator('#checkout-dialog')).toContainText('$599/mes');
  await expect(page.locator('#checkout-dialog')).toContainText('no realiza cobros');
});

async function apiMode(page) {
  await page.route('http://127.0.0.1:4173/', async route => {
    const response = await route.fetch();
    const body = (await response.text())
      .replace('name="csrf-token" content=""', 'name="csrf-token" content="test-csrf"')
      .replace('{"mode":"preview","leadEndpoint":"","checkout":{}}', '{"mode":"live","leadEndpoint":"/test-leads","checkout":{}}');
    await route.fulfill({ response, body });
  });
}
test('backend adapter submits the contract, handles 422 and retries successfully', async ({ page }) => {
  await apiMode(page);
  let calls = 0;
  await page.route('**/test-leads', async route => {
    calls++;
    expect(route.request().headers()['x-csrf-token']).toBe('test-csrf');
    expect(route.request().postDataJSON()).toEqual({ parent_name: 'Ana', channel: 'email', contact: 'ana@example.com', source: 'digizen_landing' });
    await route.fulfill({ status: calls === 1 ? 422 : 200, contentType: 'application/json', body: JSON.stringify(calls === 1 ? { errors: { contact: ['Este correo requiere revisión.'] } } : { status: 'sent' }) });
  });
  await page.goto('/');
  const form = page.locator('main [data-ada-form]');
  await form.locator('[name="parent_name"]').fill('Ana');
  await form.locator('[name="contact"]').fill('ana@example.com');
  await form.locator('[type="submit"]').click();
  await expect(form.locator('[data-error="contact"]')).toContainText('requiere revisión');
  await form.locator('[type="submit"]').click();
  await expect(form.locator('.form-status')).toContainText('está en camino');
  expect(calls).toBe(2);
});

test('a successful HTTP response without delivery confirmation is not presented as sent', async ({ page }) => {
  await apiMode(page);
  await page.route('**/test-leads', route => route.fulfill({ status: 200, contentType: 'application/json', body: '{}' }));
  await page.goto('/');
  const form = page.locator('main [data-ada-form]');
  await form.locator('[name="parent_name"]').fill('Ana');
  await form.locator('[name="contact"]').fill('ana@example.com');
  await form.locator('[type="submit"]').click();
  await expect(form.locator('.form-status')).toContainText('no pudimos confirmar');
});

test('reduced motion, anchors and native accordion stay operable', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/');
  await page.locator('.dg-nav__links a[href="#beat-55-title"]').click();
  await expect(page.locator('#beat-55-title')).toBeFocused();
  const details = page.locator('[data-block="beat-3"] details').first();
  await details.locator('summary').click();
  await expect(details).toHaveAttribute('open', '');
  await details.locator('summary').click();
  await expect(details).not.toHaveAttribute('open', '');
});
