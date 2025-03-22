import { getProfile } from '../profile.js';
import { loadPage } from '../router/router.js';
import { loadFriends } from './friends.js';
import { loadRequests } from './requests.js';

document.addEventListener('click', async function (event) {
  event.preventDefault();
  if (event.target && event.target.id === 'my-profile-btn') {
    await loadPage('/profile');
    await getProfile();
  } else if (event.target && event.target.id === 'friends-btn') {
    await loadPage('/friends');
    await loadFriends();
  } else if (event.target && event.target.id === 'requests-btn') {
    await loadPage('/requests');
    await loadRequests();
  }
});
