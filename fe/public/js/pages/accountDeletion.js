import { usersService } from '../services/users.js';
import { loadPage } from '../router/router.js';

export function accountDeletion() {
  const form = document.getElementById('accountDeletionForm');
  const passwordInput = document.getElementById('password');
  const togglePassword = document.getElementById('togglePassword');

  form.addEventListener('formValid', async () => {
    const ok = await usersService.deleteUser(passwordInput.value);
    if (ok) {
      loadPage('/auth');
    }
  });

  togglePassword?.addEventListener('click', () => {
    passwordInput.type =
      passwordInput.type === 'password' ? 'text' : 'password';
  });
}
