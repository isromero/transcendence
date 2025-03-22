import { editUsername } from './editUsername.js';
import { editPassword } from './editPassword.js';
import { usersService } from '../services/users.js';
import { loadPage } from '../router/router.js';
import { showErrorToast } from '../utils/helpers.js';

const avatarInput = document.getElementById('avatarInput');

document.addEventListener('click', async event => {
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
  } else if (target.matches('#changeAvatarButton')) {
    avatarInput.click();
  } else if (target.matches('#accountDeletionButton')) {
    event.preventDefault();
    const ok = await usersService.deleteUser();
    if (ok) {
      loadPage('/auth');
    }
  }
});

avatarInput.addEventListener('change', async event => {
  const file = event.target.files[0];

  // Can upload only images
  if (!file.type.startsWith('image/')) {
    showErrorToast('Only images supported');
    return;
  }

  const maxSize = 5 * 1024 * 1024; // 5MB
  if (file.size > maxSize) {
    showErrorToast('Image size should be less than 5MB');
    return;
  }

  await usersService.updateUserAvatar(file);
});
