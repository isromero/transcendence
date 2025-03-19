import { getProfile } from '../profile.js';
import { loadPage } from '../router/router.js';
document.addEventListener('click', async function (event) {
  event.preventDefault();
  if (event.target && event.target.id === 'my-profile-btn') {
    await loadPage('/profile');
    await getProfile();
  }
});
