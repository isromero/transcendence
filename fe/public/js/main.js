import { loadPage } from './router/router.js';
import { getCleanPageKey } from './utils/helpers.js';
import { checkAuth } from './utils/auth-middleware.js';
import { usersService } from './services/users.js';

document.addEventListener('DOMContentLoaded', async () => {
  const initialPath = window.location.pathname;
  if (checkAuth(initialPath)) {
    await loadPage(initialPath);
    await usersService.updateOnlineStatus(true);
  }
});

window.addEventListener('popstate', async event => {
  const rawPage = event.state?.page || window.location.pathname;
  const cleanPage = getCleanPageKey(rawPage);

  if (checkAuth(cleanPage)) {
    await loadPage(cleanPage);
  }
});

document.body.addEventListener('click', async event => {
  const modalLink = event.target.closest('[data-modal]');
  const spaLink = event.target.closest('.spa-link');

  if (modalLink) {
    event.preventDefault();
    const modalPage = modalLink.getAttribute('data-modal');
    await loadPage(`/modal-${modalPage}`);
  } else if (spaLink) {
    event.preventDefault();
    const page = spaLink.getAttribute('href');

    if (checkAuth(page)) {
      await loadPage(page);
    }
  }
});

// TODO: THIS IS NOT WORKING. When user are closing the tab, user have to be offline
window.addEventListener('beforeunload', async () => {
  await usersService.updateOnlineStatus(false);
});

// When user comeback to the tab, ser have to be online
document.addEventListener('visibilitychange', async () => {
  if (document.visibilityState === 'visible') {
    await usersService.updateOnlineStatus(true);
  } else {
    await usersService.updateOnlineStatus(false);
  }
});
