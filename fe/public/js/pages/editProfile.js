import { editUsername } from './editUsername.js';
import { editPassword } from './editPassword.js';

document.addEventListener('click', event => {
  const target = event.target;

  if (target.matches('#changeUsernameButton')) {
    event.preventDefault();
    document.addEventListener('spaContentLoaded', () => editUsername(), {
      once: true,
    });
  } else if (target.matches('#changePasswordButton')) {
    event.preventDefault();
    document.addEventListener('spaContentLoaded', () => editPassword(), {
      once: true,
    });
  }
});
