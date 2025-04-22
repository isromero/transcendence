import { authService } from '../services/auth.js';
import { loadPage } from '../router/router.js';

export function init() {
  async function handleLogout() {
    const success = await authService.logout();
    if (success) {
      await loadPage('/auth', { updateHistory: false });
    }
  }

  const logoutButton = document.getElementById('confirm-logout-btn');
  logoutButton?.addEventListener('click', handleLogout);

  return () => {
    logoutButton?.removeEventListener('click', handleLogout);
  };
}
