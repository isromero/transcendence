import { editUsername } from './editUsername.js';
import { editPassword } from './editPassword.js';
import { usersService } from '../services/users.js';
import { loadPage } from '../router/router.js';
import { profileService } from '../services/profile.js';


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



export async function hiddeByUsernameLength() {
  const { data } = await profileService.getProfile();
  
  const username = document.getElementById("changeUsernameButton");
  const password = document.getElementById("changePasswordButton");

  console.log(data.username);
  if (data.username.length > 8) {
      username.hidden = !username.hidden;
      password.hidden = !password.hidden;
  }
}
// if (
//   document.readyState !== 'loading' &&
//   window.location.pathname.includes('/profile')
// ) {
//   await hiddeByUsernameLength();
// }
await hiddeByUsernameLength();

