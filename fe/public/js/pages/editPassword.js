import { usersService } from '../services/users.js';
import { loadPage } from '../router/router.js';

export function editPassword() {
  const form = document.getElementById('editPasswordForm');
  const usernameInput = document.getElementById('username');
  const oldPasswordInput = document.getElementById('oldPassword');
  const newPasswordInput = document.getElementById('newPassword');
  const toggleOldPassword = document.getElementById('toggleOldPassword');
  const toggleNewPassword = document.getElementById('toggleNewPassword');

  form.addEventListener('formValid', async () => {
    const user = {
      username: usernameInput.value,
      oldPassword: oldPasswordInput.value,
      newPassword: newPasswordInput.value,
    };

    const result = await usersService.updateUser(user);
    if (result) {
      await loadPage('/edit-profile');
    }
  });

  toggleOldPassword?.addEventListener('click', () => {
    oldPasswordInput.type =
      oldPasswordInput.type === 'password' ? 'text' : 'password';
  });

  toggleNewPassword?.addEventListener('click', () => {
    newPasswordInput.type =
      newPasswordInput.type === 'password' ? 'text' : 'password';
  });
}
