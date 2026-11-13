/* Content and navigation are usable without JavaScript. Only draft composition is enhanced. */
(() => {
  'use strict';
  const form = document.querySelector('#enquiry-form');
  if (form) form.hidden = false;
  if (form) form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const fields = new FormData(form);
    const message = `Sandy D. Carter enquiry\nName: ${String(fields.get('name')).trim()}\nInterest: ${fields.get('interest')}\n\n${String(fields.get('message')).trim()}`;
    const email = event.submitter?.value === 'email';
    const destination = email
      ? `mailto:rajan@houseofbrands.in?subject=${encodeURIComponent('Sandy D. Carter enquiry')}&body=${encodeURIComponent(message)}`
      : `https://wa.me/917303681194?text=${encodeURIComponent(message)}`;
    form.querySelector('.form-status').textContent = `Opening ${email ? 'your email app' : 'WhatsApp'}. Your enquiry is sent only when you press send there.`;
    window.location.assign(destination);
  });
  const menu = document.querySelector('.mobile-menu');
  if (menu) {
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.open) {
        menu.open = false;
        menu.querySelector('summary').focus();
      }
    });
    document.addEventListener('click', event => {
      if (menu.open && !menu.contains(event.target)) menu.open = false;
    });
  }
})();
