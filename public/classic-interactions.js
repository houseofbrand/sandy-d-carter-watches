const menu = document.querySelector('.menu-button');
const mobile = document.querySelector('.mobile-nav');
if (menu && mobile) {
  mobile.id = 'mobile-navigation';
  menu.setAttribute('aria-controls', mobile.id);
  const setOpen = (open) => {
    mobile.classList.toggle('open', open);
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    menu.textContent = open ? '×' : '☰';
  };
  menu.addEventListener('click', () => setOpen(!mobile.classList.contains('open')));
  mobile.addEventListener('click', (event) => {
    if (event.target.closest('a')) setOpen(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && mobile.classList.contains('open')) {
      setOpen(false);
      menu.focus();
    }
  });
  matchMedia('(max-width: 980px)').addEventListener('change', () => setOpen(false));
}

const track = (event, parameters = {}) => {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event, ...parameters });
};

document.querySelectorAll('.lead-form').forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const status = form.querySelector('.form-status');
    if (form.elements.website?.value) {
      status.textContent = 'We could not process this request.';
      return;
    }
    if (!form.reportValidity()) {
      status.textContent = 'Please complete the highlighted fields and consent checkbox.';
      return;
    }
    const fields = new FormData(form);
    const kind = form.dataset.formKind || 'Website enquiry';
    const lines = [
      `SANDY D. CARTER — ${kind}`,
      `Name: ${fields.get('name') || fields.get('business') || 'Not provided'}`,
      fields.get('business') ? `Business: ${fields.get('business')}` : '',
      fields.get('email') ? `Email: ${fields.get('email')}` : '',
      fields.get('mobile') ? `Mobile: ${fields.get('mobile')}` : '',
      fields.get('country') ? `Country: ${fields.get('country')}` : '',
      fields.get('interest') ? `Interest: ${fields.get('interest')}` : '',
      fields.get('message') ? `Message: ${fields.get('message')}` : '',
      'Consent: Yes',
      `Submitted from: ${location.href}`,
      `Time: ${new Date().toISOString()}`,
    ].filter(Boolean);
    const message = lines.join('\n');
    const channel = event.submitter?.value === 'whatsapp' ? 'whatsapp' : 'email';
    const url = channel === 'whatsapp'
      ? `https://wa.me/917303681194?text=${encodeURIComponent(message)}`
      : `mailto:rajan@houseofbrands.in?subject=${encodeURIComponent(kind)}&body=${encodeURIComponent(message)}`;
    status.textContent = `Opening ${channel === 'email' ? 'your email app' : 'WhatsApp'}. Please press send there to complete your request.`;
    track('generate_lead', { lead_type: kind, channel });
    if (channel === 'whatsapp') window.open(url, '_blank', 'noopener,noreferrer');
    else window.location.assign(url);
  });
});

document.querySelectorAll('.whatsapp-float, a[href*="wa.me/"]').forEach((link) => {
  link.addEventListener('click', () => track('whatsapp_click', { link_text: link.textContent.trim() }));
});

document.querySelectorAll('a[href="#launch-list"]').forEach((link) => {
  link.addEventListener('click', (event) => {
    const target = document.querySelector('#launch-list');
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    history.replaceState(null, '', '#launch-list');
    if (mobile?.classList.contains('open')) {
      mobile.classList.remove('open');
      menu?.setAttribute('aria-expanded', 'false');
      menu?.setAttribute('aria-label', 'Open menu');
      if (menu) menu.textContent = '☰';
    }
  });
});
