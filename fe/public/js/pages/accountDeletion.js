import { usersService } from '../services/users.js';
import { loadPage } from '../router/router.js';

export function init() {
  const form = document.getElementById('accountDeletionForm');
  const passwordInput = document.getElementById('password');
  const togglePassword = document.getElementById('togglePassword');

  async function handleFormSubmit() {
    const ok = await usersService.deleteUser(passwordInput.value);
    if (ok) {
      loadPage('/auth');
    }
  }

  function handleTogglePassword() {
    passwordInput.type =
      passwordInput.type === 'password' ? 'text' : 'password';
  }

  form?.addEventListener('formValid', handleFormSubmit);
  togglePassword?.addEventListener('click', handleTogglePassword);

  return () => {
    form?.removeEventListener('formValid', handleFormSubmit);
    togglePassword?.removeEventListener('click', handleTogglePassword);
  };
}
