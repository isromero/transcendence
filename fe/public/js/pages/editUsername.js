import { usersService } from '../services/users.js';
import { loadPage } from '../router/router.js';
import { showErrorToast } from '../utils/helpers.js';

export function init() {
  const form = document.getElementById('editUsernameForm');
  const oldUsernameInput = document.getElementById('oldUsername');
  const newUsernameInput = document.getElementById('newUsername');
  const passwordInput = document.getElementById('password');
  const togglePassword = document.getElementById('togglePassword');

  async function handleFormSubmit() {
    const newUsername = newUsernameInput.value.trim();

    if (newUsername.length < 9) {
      showErrorToast('Username must be at least 9 characters long.');
      return;
    }

    const user = {
      oldUsername: oldUsernameInput.value,
      username: newUsername,
      password: passwordInput.value,
    };

    const result = await usersService.updateUser(user);
    if (result) {
      await loadPage('/edit-profile', { updateHistory: false });
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
