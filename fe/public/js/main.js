import { loadPage } from './router/router.js';
import { getCleanPageKey } from './utils/helpers.js';
import { checkAuth } from './utils/auth-middleware.js';

document.addEventListener('DOMContentLoaded', async () => {
  const initialPath = window.location.pathname;
  if (checkAuth(initialPath)) {
    await loadPage(initialPath, { updateHistory: false });
  }
});

window.addEventListener('popstate', async event => {
  const rawPage = event.state?.page || window.location.pathname;
  const cleanPage = getCleanPageKey(rawPage);

  if (checkAuth(cleanPage)) {
    await loadPage(cleanPage, { updateHistory: false });
  }
});

document.body.addEventListener('click', async event => {
  const modalLink = event.target.closest('[data-modal]');
  const spaLink = event.target.closest('.spa-link');

  if (modalLink) {
    event.preventDefault();
    const modalPage = modalLink.getAttribute('data-modal');
    await loadPage(`/modal-${modalPage}`, { updateHistory: false });
  } else if (spaLink) {
    event.preventDefault();
    const page = spaLink.getAttribute('href');

    if (checkAuth(page)) {
      await loadPage(page);
    }
  }
});
