import { usersService } from '../services/users.js';
import { loadPage } from '../router/router.js';

export function editUsername() {
  const form = document.getElementById('editUsernameForm');
  const oldUsernameInput = document.getElementById('oldUsername');
  const newUsernameInput = document.getElementById('newUsername');
  const passwordInput = document.getElementById('password');
  const togglePassword = document.getElementById('togglePassword');

  form.addEventListener('formValid', async () => {
    const user = {
      oldUsername: oldUsernameInput.value,
      username: newUsernameInput.value,
      password: passwordInput.value,
    };

    const result = await usersService.updateUser(user);
    if (result) {
      await loadPage('/edit-profile');
    }
  });

  togglePassword.addEventListener('click', () => {
    passwordInput.type =
      passwordInput.type === 'password' ? 'text' : 'password';
  });
}
