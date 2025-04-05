import { usersService } from '../services/users.js';
import { showErrorToast } from '../utils/helpers.js';

export function init() {

  // TODO: wtf is this
  export function hideByUsernameLength() {
    const { data } = await profileService.getProfile();

    const username = document.getElementById("changeUsernameButton");
    const password = document.getElementById("changePasswordButton");

    console.log(data.username);
    if (data.username.length > 8) {
        username.hidden = !username.hidden;
        password.hidden = !password.hidden;
    }
  }
  
  hideByUsernameLength();

  
  const avatarInput = document.getElementById('avatarInput');
  const changeAvatarButton = document.getElementById('changeAvatarButton');
  const MAX_SIZE = 5 * 1024 * 1024; // 5MB

  async function handleAvatarChange(event) {
    const file = event.target.files[0];

    // Can upload only images
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
