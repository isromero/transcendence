import { loadPage } from '../router/router.js';
import { friendsService } from '../services/friends.js';

const form = document.getElementById('addFriendForm');
const usernameInput = document.getElementById('usernameInput');

form.addEventListener('formValid', async () => {
  const friend = {
    username: usernameInput.value,
  };

  const result = await friendsService.addFriend(friend);
  if (result) {
    await loadPage('/friends');
  }
});
