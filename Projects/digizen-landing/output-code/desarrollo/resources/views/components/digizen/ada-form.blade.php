<form class="ada-form" aria-label="Formulario Conversa con ADA" data-ada-form novalidate>
  <h3>Conversa con ADA</h3>
  <p class="form-intro">Formulario de datos del adulto.</p>
  <label class="form-field">
    <span>Nombre del papá o mamá</span>
    <input name="parent_name" autocomplete="name" required maxlength="100" placeholder="Tu nombre" aria-describedby="name-error-inline">
    <span class="field-error" id="name-error-inline" data-error="parent_name"></span>
  </label>
  <fieldset class="channel-fieldset">
    <legend>Canal de entrega</legend>
    <div class="channel-selector">
      <label><input type="radio" name="channel" value="email" checked><span>Correo</span></label>
      <label><input type="radio" name="channel" value="whatsapp"><span>WhatsApp</span></label>
    </div>
  </fieldset>
  <label class="form-field">
    <span data-contact-label>Correo electrónico</span>
    <input name="contact" type="email" inputmode="email" autocomplete="email" required maxlength="254" placeholder="nombre@correo.com" aria-describedby="contact-hint-inline contact-error-inline">
    <span class="field-hint" id="contact-hint-inline" data-contact-hint>Recibirás aquí tu liga de acceso a ADA.</span>
    <span class="field-error" id="contact-error-inline" data-error="contact"></span>
  </label>
  <button class="dg-button form-submit" type="submit" data-btn><span class="submit-label">💬 Conversa con ADA</span><span class="submit-busy" hidden>Enviando…</span></button>
  <p class="form-delivery-note">Se manda la liga de acceso; no abre WhatsApp directo.</p>
  <p class="form-preview-note" data-preview-note hidden>Vista previa: puedes probar el formulario. No se enviará ningún mensaje.</p>
  <div class="form-status" role="status" aria-live="polite" tabindex="-1" hidden></div>
  <noscript><p>Activa JavaScript para completar este formulario.</p></noscript>
</form>
