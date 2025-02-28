import { changeSettings } from '../pages/changeSettings.js';
import { showErrorToast } from '../utils/helpers.js';
const changeUser = document.getElementById('changeUserForm');
const changeMail = document.getElementById('changeMailForm');
const changePassword = document.getElementById('changePasswordForm');

changeUser.addEventListener('formValid', async () => {
  const user = {
    username: document.getElementById('username').value,
    password: document.getElementById('password').value,
  };

  if (user.password !== user.password_confirmation) {
    showErrorToast('Passwords do not match');
    return;
  }

  await changeSettings.changeUser(user.username, user.password);
});


changeMail.addEventListener('formValid', async () => {
    const user = {
      email: document.getElementById('email').value,
      username: document.getElementById('username').value,
      password: document.getElementById('password').value,
      password_confirmation: document.getElementById('password-confirmation')
        .value,
    };
  
    if (user.password !== user.password_confirmation) {
      showErrorToast('Passwords do not match');
      return;
    }
  
    await changeSettings.changeUser(user.username, user.password);
  });


changePassword.addEventListener('formValid', async () => {
    const user = {
      email: document.getElementById('email').value,
      username: document.getElementById('username').value,
      password: document.getElementById('password').value,
      password_confirmation: document.getElementById('password-confirmation')
        .value,
    };
  
    if (user.password !== user.password_confirmation) {
      showErrorToast('Passwords do not match');
      return;
    }
  
    await changeSettings.changeUser(user.username, user.password);
  });
