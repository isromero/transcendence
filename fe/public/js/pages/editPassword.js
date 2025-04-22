import { usersService } from '../services/users.js';
import { loadPage } from '../router/router.js';

export function init() {
  const form = document.getElementById('editPasswordForm');
  const usernameInput = document.getElementById('username');
  const oldPasswordInput = document.getElementById('oldPassword');
  const newPasswordInput = document.getElementById('newPassword');
  const toggleOldPassword = document.getElementById('toggleOldPassword');
  const toggleNewPassword = document.getElementById('toggleNewPassword');

  async function handleFormSubmit() {
    const user = {
      username: usernameInput.value,
      oldPassword: oldPasswordInput.value,
      newPassword: newPasswordInput.value,
    };

    const result = await usersService.updateUser(user);
    if (result) {
      await loadPage('/edit-profile', { updateHistory: false });
    }
  }

  function handleToggleOldPassword() {
    oldPasswordInput.type =
      oldPasswordInput.type === 'password' ? 'text' : 'password';
  }

  function handleToggleNewPassword() {
    newPasswordInput.type =
      newPasswordInput.type === 'password' ? 'text' : 'password';
  }

  form?.addEventListener('formValid', handleFormSubmit);
  toggleOldPassword?.addEventListener('click', handleToggleOldPassword);
  toggleNewPassword?.addEventListener('click', handleToggleNewPassword);

  return () => {
    form?.removeEventListener('formValid', handleFormSubmit);
    toggleOldPassword?.removeEventListener('click', handleToggleOldPassword);
    toggleNewPassword?.removeEventListener('click', handleToggleNewPassword);
  };
}
