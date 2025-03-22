import { logout } from './logout.js';

document.addEventListener('click', async event => {
  event.preventDefault();
  const target = event.target;

  if (target.matches('#confirm-logout-btn')) {
    await logout();
  }
});
