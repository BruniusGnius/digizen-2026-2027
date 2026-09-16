export function validateLead({ parent_name = '', channel = 'email', contact = '' }) {
  const errors = {};
  const name = parent_name.trim();
  if (name.length < 2 || name.length > 100 || !/\p{L}/u.test(name)) errors.parent_name = 'Escribe tu nombre (al menos dos caracteres).';
  if (!['email', 'whatsapp'].includes(channel)) errors.channel = 'Selecciona un canal de entrega.';
  if (channel === 'email' && (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact.trim()) || contact.length > 254)) errors.contact = 'Escribe un correo electrónico válido.';
  if (channel === 'whatsapp' && !/^\+[1-9]\d{7,14}$/.test(contact.replace(/[\s()-]/g, ''))) errors.contact = 'Incluye el código de país. Por ejemplo: +52 55 1234 5678.';
  return errors;
}

export function leadPayload(values) {
  return {
    parent_name: values.parent_name.trim(),
    channel: values.channel,
    contact: values.channel === 'whatsapp' ? values.contact.replace(/[\s()-]/g, '') : values.contact.trim(),
    source: 'digizen_landing',
  };
}

export function serverError(status) {
  if (status === 429) return 'Hubo varios intentos seguidos. Espera un momento y vuelve a intentarlo.';
  if (status === 419) return 'La sesión venció. Recarga la página antes de volver a intentarlo.';
  if (status === 422) return 'Revisa los datos indicados antes de continuar.';
  return 'No pudimos confirmar el envío. Tus datos siguen aquí; puedes volver a intentarlo.';
}
