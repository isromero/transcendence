import { changeSettings } from '../pages/changeSettings.js';
import { showErrorToast } from '../utils/helpers.js';
const changeUser = document.getElementById('changeUserForm');
const changeMail = document.getElementById('changeMailForm');
const changePassword = document.getElementById('changePasswordForm');

changeUser.addEventListener('formValid', async () => {
  const user = {
    username: document.getElementById('new-username').value,
    password: document.getElementById('password').value,
  };
  await changeSettings.changeUser(user.username, user.password);
});


changePassword.addEventListener('formValid', async () => {
    const user = {
      password: document.getElementById('password').value,
      password_confirmation: document.getElementById('password-confirmation')
        .value,
    };
    await changeSettings.changePassword(user.username, user.password);
  });
