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
