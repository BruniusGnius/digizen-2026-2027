(function () {
  'use strict';
  var variant = location.pathname.indexOf('/a/') === 0 ? 'A' : location.pathname.indexOf('/b/') === 0 ? 'B' : null;
  if (!variant) return;
  var experiment = 'digizen_landing_ab_2026_10';
  var landing = variant === 'A' ? 'digizen-landing' : 'digizen-landing-b-v04-claude';
  var visitorKey = experiment + '_visitor_id';
  var variantKey = experiment + '_variant';
  var started = performance.now();
  var lastSection = null;
  var seenSections = Object.create(null);
  var seenDepths = Object.create(null);
  var attributionKey = experiment + '_attribution';
  function getLocal(key) {
    try {
      var expiry = Number(localStorage.getItem(key + '_expires_at'));
      return expiry > Date.now() ? localStorage.getItem(key) : null;
    } catch (_) { return null; }
  }
  function setLocal(key, value) {
    try {
      localStorage.setItem(key, value);
      localStorage.setItem(key + '_expires_at', String(Date.now() + 90 * 86400000));
    } catch (_) {}
  }
  function cookie(key) {
    var row = document.cookie.split('; ').find(function (x) { return x.indexOf(key + '=') === 0; });
    return row ? decodeURIComponent(row.slice(key.length + 1)) : null;
  }
  function saveCookie(key, value) {
    document.cookie = key + '=' + encodeURIComponent(value) + '; Max-Age=7776000; Path=/; SameSite=Lax; Secure';
  }
  setLocal(variantKey, variant); saveCookie(variantKey, variant);
  var visitor = getLocal(visitorKey) || cookie(visitorKey);
  if (!visitor || !/^[a-zA-Z0-9_-]{8,100}$/.test(visitor)) {
    visitor = 'anon_' + (crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(36).slice(2));
  }
  setLocal(visitorKey, visitor); saveCookie(visitorKey, visitor);
  var search = new URLSearchParams(location.search);
  var attr = {};
  try { attr = JSON.parse(getLocal(attributionKey) || '{}'); } catch (_) {}
  ['source', 'medium', 'campaign', 'content', 'term'].forEach(function (key) {
    var value = search.get('utm_' + key);
    if (value) attr['utm_' + key] = value.slice(0, 150);
  });
  setLocal(attributionKey, JSON.stringify(attr));

  // Clarity solo observa estas landings para adultos. Los tags nunca incluyen contacto.
  if (location.hostname === 'digizen.gnius.club' || location.hostname === 'digizen-demo.gnius.club') {
    document.querySelectorAll('[data-digizen-lead]').forEach(function (form) {
      form.setAttribute('data-clarity-mask', 'True');
    });
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, 'clarity', 'script', 'yx8hr2als5');
    window.clarity('set', 'digizen_variant', variant);
    window.clarity('set', 'digizen_landing_id', landing);
    window.clarity('set', 'digizen_environment', location.hostname === 'digizen-demo.gnius.club' ? 'preview' : 'production');
  }

  function base(extra) {
    var b = Object.assign({
      experiment_key: experiment, variant: variant, landing_id: landing, visitor_id: visitor,
      path: location.pathname, device_type: matchMedia('(max-width: 767px)').matches ? 'mobile' : 'desktop',
      elapsed_ms: Math.round(performance.now() - started)
    }, attr, extra || {});
    var lead = getLocal(experiment + '_lead_id');
    if (lead && /^\d+$/.test(lead)) b.lead_id = Number(lead);
    return b;
  }
  function capture(event, extra) {
    var payload = base(Object.assign({ event_name: event }, extra || {}));
    fetch('/api/events.php', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload), credentials: 'same-origin', keepalive: true
    }).catch(function () {});
  }
  window.DigizenAB = { capture: capture, base: base, variant: variant, landingId: landing };
  window.addEventListener('digizen:cookie-preferences', function (event) {
    var detail = event.detail || {};
    var categories = detail.categories;
    if (!categories || typeof categories.performance !== 'boolean' || typeof categories.marketing !== 'boolean') return;
    fetch('/api/consents.php', { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(base({ action: detail.action === 'revoked' ? 'revoked' : 'accepted', categories: categories,
        entry_url: location.href.slice(0, 500) })), credentials: 'same-origin', keepalive: true }).catch(function () {});
  });

  var observed = new WeakSet();
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var id = el.getAttribute('data-nav-section') || el.id || el.getAttribute('data-pin');
        if (!id || seenSections[id]) return;
        seenSections[id] = true;
        var heading = el.querySelector('h1,h2,h3');
        var label = heading ? (heading.textContent || '').trim().slice(0, 255) : id;
        lastSection = id;
        if (window.clarity) window.clarity('set', 'digizen_last_section', id);
        capture(location.pathname.includes('reglas-de-ada') ? 'rules_section_reached' : 'section_reached', {
          section_id: id, section_label: label
        });
        if (/precio|oferta|inscrip|P-11/i.test(id + ' ' + label)) {
          capture('pricing_reached', { section_id: id, section_label: label });
        }
      });
    }, { threshold: 0.25 }) : null;
  function observeSections() {
    // El diálogo de A usa una expresión Angular que devuelve false para clics
    // interiores. Angular cancela entonces la acción por defecto del checkbox.
    // Detener la propagación antes de llegar al diálogo conserva los controles.
    var adaDialogInner = document.querySelector('.dg-dialog .dg-dialog-inner');
    if (adaDialogInner && !adaDialogInner.dataset.digizenClickGuard) {
      adaDialogInner.dataset.digizenClickGuard = 'true';
      adaDialogInner.addEventListener('click', function (event) { event.stopPropagation(); });
    }
    if (!io) return;
    var nodes = document.querySelectorAll('section[id], [data-nav-section], [data-pin], .rules-section[id]');
    nodes.forEach(function (node) {
      if (!observed.has(node)) { observed.add(node); io.observe(node); }
    });
  }
  var observeTimer;
  new MutationObserver(function () { clearTimeout(observeTimer); observeTimer = setTimeout(observeSections, 200); })
    .observe(document.documentElement, { childList: true, subtree: true });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', observeSections, { once: true });
  else observeSections();
  var marks = [25, 50, 75, 90, 100];
  addEventListener('scroll', function () {
    var max = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    var pct = Math.min(100, Math.round(scrollY / max * 100));
    marks.forEach(function (mark) {
      if (pct >= mark && !seenDepths[mark]) {
        seenDepths[mark] = true;
        capture('scroll_depth_reached', { section_id: lastSection, scroll_depth: mark });
      }
    });
  }, { passive: true });
  document.addEventListener('click', function (event) {
    var target = event.target.closest('a, button, summary');
    if (!target) return;
    var action = target.getAttribute('data-action') || '';
    var href = target.getAttribute('href') || '';
    if (/reglas-de-ada/i.test(href) || /reglas de ada/i.test(target.textContent || '')) {
      capture('rules_opened', { section_id: lastSection });
    }
    if (target.tagName === 'SUMMARY') capture('faq_opened', { section_id: lastSection });
    if (action === 'ada' || /convers(a|ar) con ada/i.test(target.textContent || '')) {
      capture('ada_request_opened', { section_id: lastSection, cta: 'ada' });
    }
    if (location.pathname.includes('reglas-de-ada') && (action || href)) {
      capture('rules_cta_clicked', { section_id: lastSection, cta: action || 'link' });
    }
    if (action || href) capture('cta_clicked', { section_id: lastSection, cta: action || 'link', plan: target.getAttribute('data-plan') });
  }, true);
  window.addEventListener('digizen:checkout', function (event) {
    capture('checkout_started', { plan: event.detail && event.detail.plan || null });
    if (['localhost', '127.0.0.1', 'digizen-demo.gnius.club'].includes(location.hostname)) {
      var notice = document.getElementById('digizen-qa-checkout-notice');
      if (!notice) {
        notice = document.createElement('div');
        notice.id = 'digizen-qa-checkout-notice';
        notice.setAttribute('role', 'status');
        notice.style.cssText = 'position:fixed;z-index:2147483647;left:16px;right:16px;bottom:16px;max-width:540px;margin:auto;padding:16px 20px;border-radius:12px;background:#17243b;color:#fff;font:500 16px/1.45 system-ui;box-shadow:0 8px 30px #0004';
        document.body.appendChild(notice);
      }
      notice.textContent = 'La compra aún no está disponible en esta prueba. No se realizará ningún cobro.';
    }
  });

  document.addEventListener('submit', function (event) {
    var form = event.target;
    if (!form.matches('[data-digizen-lead]')) return;
    event.preventDefault();
    if (!form.reportValidity()) return;
    var name = form.querySelector('[name=name]');
    var email = form.querySelector('[name=email]');
    var phone = form.querySelector('[name=phone]');
    var contact = form.querySelector('[name=contact]');
    var channel = form.getAttribute('data-channel-active') || form.closest('[data-channel-active]')?.getAttribute('data-channel-active') || '';
    var emailValue = email ? email.value.trim() : (channel === 'correo' && contact ? contact.value.trim() : '');
    var phoneValue = phone ? phone.value.trim() : (channel === 'whatsapp' && contact ? contact.value.trim() : '');
    if (!emailValue && !phoneValue) { alert('Escribe tu correo o WhatsApp.'); return; }
    if (emailValue && phoneValue) { alert('Elige solo un canal: correo o WhatsApp. Deja el otro campo vacío.'); return; }
    if (!channel) {
      var selected = form.querySelector('[name=preferred_channel]');
      channel = emailValue && phoneValue && selected ? selected.value : (emailValue ? 'correo' : 'whatsapp');
    }
    var privacy = form.querySelector('[name=privacy_accepted]');
    var terms = form.querySelector('[name=terms_accepted]');
    var marketing = form.querySelector('[name=marketing_consent]');
    if (!terms || !terms.checked) { alert('Acepta los Términos y condiciones para continuar.'); return; }
    if (!privacy || !privacy.checked) { alert('Confirma que leíste el aviso de privacidad.'); return; }
    if (location.hostname === 'digizen-demo.gnius.club') {
      if (!/^QA\s/.test(name ? name.value.trim() : '')) {
        alert('Esta demo solo acepta nombres de prueba que empiecen por «QA » (por ejemplo, «QA Bruno»). No se guardó tu solicitud.');
        return;
      }
      if (emailValue && !/^bruno\+[a-z0-9._-]+@gnius\.club$/i.test(emailValue)) {
        alert('Esta demo solo acepta correos de prueba como bruno+ada_qa@gnius.club. No se guardó tu solicitud.');
        return;
      }
      if (phoneValue && phoneValue.replace(/\D/g, '') !== '525500000000') {
        alert('Esta demo solo acepta el WhatsApp ficticio +52 55 0000 0000. No se guardó tu solicitud.');
        return;
      }
    }
    var submit = form.querySelector('[type=submit]');
    if (submit) submit.disabled = true;
    var data = base({
      name: name ? name.value.trim() : '', email: emailValue || null, phone: phoneValue || null,
      preferred_channel: channel, terms_accepted: true, privacy_accepted: true, marketing_consent: Boolean(marketing && marketing.checked),
      entry_url: location.href.slice(0, 500), referrer_url: document.referrer.slice(0, 500),
      referral_code: search.get('ref') || null
    });
    fetch('/api/leads.php', { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data), credentials: 'same-origin' })
      .then(function (response) { return response.json().then(function (body) { if (!response.ok) throw Error(body.error || 'error'); return body; }); })
      .then(function (body) {
        setLocal(experiment + '_lead_id', String(body.lead_id));
        capture('ada_request_submitted', { section_id: lastSection });
        sessionStorage.setItem('digizen_demo_confirmation', JSON.stringify({
          demo_url: body.demo_url, demo_simulated: body.demo_simulated === true,
          public_code: body.public_code, variant: variant, landing_id: landing
        }));
        location.href = '/demo-ada-confirmado/';
      })
      .catch(function (error) {
        var message = error && error.message === 'preview_qa_only'
          ? 'Esta demo solo acepta datos QA: nombre que empiece por «QA », correo bruno+...@gnius.club o WhatsApp ficticio +52 55 0000 0000.'
          : error && error.message === 'choose_one_contact_method'
            ? 'Elige solo un canal: correo o WhatsApp. Deja el otro campo vacío.'
          : error && error.message === 'demo_not_configured'
            ? 'El acceso de prueba a ADA no está configurado en este momento.'
            : 'No pudimos registrar tu solicitud. Inténtalo de nuevo.';
        alert(message);
      })
      .finally(function () { if (submit) submit.disabled = false; });
  }, true);
  capture(location.pathname.includes('reglas-de-ada') ? 'rules_opened' : 'page_view');
})();
