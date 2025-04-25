import { usersService } from '../services/users.js';
import { showErrorToast } from '../utils/helpers.js';
import { profileService } from '../services/profile.js';
export async function init() {
  async function hackToDontShowEditableFieldsFor42Users() {
    const { data } = await profileService.getProfile();

    const username = document.getElementById('changeUsernameButton');
    const password = document.getElementById('changePasswordButton');

    username.hidden = false;
    password.hidden = false;

    if (data.username.length < 9) {
      username.hidden = true;
      password.hidden = true;
    }
  }

  await hackToDontShowEditableFieldsFor42Users();

  const avatarInput = document.getElementById('avatarInput');
  const changeAvatarButton = document.getElementById('changeAvatarButton');
  const MAX_SIZE = 5 * 1024 * 1024; // 5MB

  async function handleAvatarChange(event) {
    const file = event.target.files[0];

    if (!file.type.startsWith('image/')) {
      showErrorToast('Only images supported');
      return;
    }

    if (file.size > MAX_SIZE) {
      showErrorToast('Image size should be less than 5MB');
      return;
    }

    await usersService.updateUserAvatar(file);
  }

  function handleChangeAvatarClick() {
    avatarInput?.click();
  }

  avatarInput?.addEventListener('change', handleAvatarChange);
  changeAvatarButton?.addEventListener('click', handleChangeAvatarClick);

  return () => {
    avatarInput?.removeEventListener('change', handleAvatarChange);
    changeAvatarButton?.removeEventListener('click', handleChangeAvatarClick);
  };
}
