import { editUsername } from './editUsername.js';
import { editPassword } from './editPassword.js';
import { usersService } from '../services/users.js';
import { loadPage } from '../router/router.js';

document.addEventListener('click', async event => {
  event.preventDefault();

  const target = event.target;

  if (target.matches('#changeUsernameButton')) {
    document.addEventListener('spaContentLoaded', () => editUsername(), {
      once: true,
    });
  } else if (target.matches('#changePasswordButton')) {
    document.addEventListener('spaContentLoaded', () => editPassword(), {
      once: true,
    });
  } else if (target.matches('#accountDeletionButton')) {
    const ok = await usersService.deleteUser();
    if (ok) {
      loadPage('/auth');
    }
  }
});
