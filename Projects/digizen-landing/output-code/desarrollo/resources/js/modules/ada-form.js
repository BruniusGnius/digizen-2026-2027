import { validateLead, leadPayload, serverError } from '../lib/lead';

export function setupForm(form, config) {
  const name = form.elements.parent_name;
  const contact = form.elements.contact;
  const submit = form.querySelector('[type="submit"]');
  const status = form.querySelector('.form-status');
  const channel = () => form.querySelector('[name="channel"]:checked').value;
  const values = () => ({ parent_name: name.value, contact: contact.value, channel: channel() });
  const contactValues = { email: '', whatsapp: '' };
  let previousChannel = channel();
  let pending = false;
  let controller;
  form.querySelector('[data-preview-note]').hidden = config.mode !== 'preview';
  function showStatus(message, kind = 'success') {
    status.textContent = message;
    status.dataset.kind = kind;
    status.hidden = false;
  }
  function showErrors(errors) {
    form.querySelectorAll('[data-error]').forEach(element => { element.textContent = errors[element.dataset.error] || ''; });
    [name, contact].forEach(input => input.setAttribute('aria-invalid', String(Boolean(errors[input.name]))));
  }
  form.querySelectorAll('[name="channel"]').forEach(radio => radio.addEventListener('change', () => {
    contactValues[previousChannel] = contact.value;
    previousChannel = channel();
    contact.value = contactValues[previousChannel];
    const email = previousChannel === 'email';
    contact.type = email ? 'email' : 'tel';
    contact.inputMode = email ? 'email' : 'tel';
    contact.autocomplete = email ? 'email' : 'tel';
    contact.placeholder = email ? 'nombre@correo.com' : '+52 55 1234 5678';
    form.querySelector('[data-contact-label]').textContent = email ? 'Correo electrónico' : 'Número de WhatsApp';
    form.querySelector('[data-contact-hint]').textContent = email ? 'Recibirás aquí tu liga de acceso a ADA.' : 'Incluye el código de país. Recibirás aquí tu liga de acceso a ADA.';
    showErrors({});
    status.hidden = true;
  }));
  [name, contact].forEach(input => input.addEventListener('input', () => {
    if (input.getAttribute('aria-invalid') === 'true') {
      const errors = validateLead(values());
      form.querySelector(`[data-error="${input.name}"]`).textContent = errors[input.name] || '';
      input.setAttribute('aria-invalid', String(Boolean(errors[input.name])));
    }
    status.hidden = true;
  }));
  const busy = (active) => {
    pending = active;
    form.setAttribute('aria-busy', String(active));
    submit.disabled = active;
    [name, contact, ...form.querySelectorAll('[name="channel"]')].forEach(input => { input.disabled = active; });
    form.querySelector('.submit-label').hidden = active;
    form.querySelector('.submit-busy').hidden = !active;
  };
  form.cancelRequest = () => controller?.abort();
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (pending) return;
    status.hidden = true;
    const data = values();
    const errors = validateLead(data);
    showErrors(errors);
    if (Object.keys(errors).length) { form.querySelector('[aria-invalid="true"]')?.focus(); return; }
    if (config.mode === 'preview') {
      showStatus('Los datos son válidos. Prueba completada: no se enviaron ni se guardaron tus datos.');
      status.focus();
      return;
    }
    const token = document.querySelector('meta[name="csrf-token"]')?.content;
    let endpoint;
    try { endpoint = new URL(config.leadEndpoint, location.origin); } catch { /* Handled below. */ }
    if (!config.leadEndpoint || !token || endpoint?.origin !== location.origin) {
      showStatus('El acceso no está disponible por el momento. Inténtalo más tarde.', 'error');
      return;
    }
    const payload = leadPayload(data);
    busy(true);
    controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);
    try {
      const response = await fetch(endpoint, {
        method: 'POST', credentials: 'same-origin', signal: controller.signal,
        headers: { 'Content-Type': 'application/json', Accept: 'application/json', 'X-CSRF-TOKEN': token },
        body: JSON.stringify(payload),
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) {
        if (response.status === 422 && result.errors) {
          const allowed = {};
          for (const field of ['parent_name', 'contact']) {
            const value = result.errors[field];
            const message = Array.isArray(value) ? value[0] : value;
            if (typeof message === 'string') allowed[field] = message;
          }
          showErrors(allowed);
        }
        showStatus(serverError(response.status), 'error');
      } else if (result.status === 'sent') {
        showStatus(data.channel === 'email' ? 'Tu liga de acceso está en camino. Revisa tu correo electrónico.' : 'Tu liga de acceso está en camino. Revisa tu WhatsApp.');
      } else {
        showStatus('Recibimos una respuesta, pero no pudimos confirmar el envío. Inténtalo de nuevo más tarde.', 'error');
      }
    } catch (error) {
      showStatus(error.name === 'AbortError' ? 'El envío no se pudo confirmar a tiempo. Puedes volver a intentarlo.' : 'No pudimos conectar. Revisa tu conexión y vuelve a intentarlo.', 'error');
    } finally {
      clearTimeout(timeout);
      busy(false);
      if (!form.closest('dialog') || form.closest('dialog').open) {
        const invalid = form.querySelector('[aria-invalid="true"]');
        (invalid || status).focus();
      }
    }
  });
}
