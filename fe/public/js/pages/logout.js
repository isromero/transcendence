import { authService } from '../services/auth.js';
import { loadPage } from '../router/router.js';

export async function logout() {
  const success = await authService.logout();
  if (success) {
    await loadPage('/auth');
  }
}
