import { loadPage } from './router/router.js';
import { getCleanPageKey } from './utils/helpers.js';

document.addEventListener('DOMContentLoaded', () => {
  loadPage(window.location.pathname);
});

window.addEventListener('popstate', event => {
  const rawPage = event.state?.page || window.location.pathname;
  loadPage(getCleanPageKey(rawPage));
});

document.body.addEventListener('click', event => {
  const modalLink = event.target.closest('[data-modal]');
  const spaLink = event.target.closest('.spa-link');

  if (modalLink) {
    event.preventDefault();
    const modalPage = modalLink.getAttribute('data-modal');
    loadPage(`/modal-${modalPage}`);
  } else if (spaLink) {
    event.preventDefault();
    const page = spaLink.getAttribute('href');
    loadPage(page);
  }
});
