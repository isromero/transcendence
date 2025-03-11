import { loadPage } from '../router/router.js';
import { friendsService } from '../services/friends.js';

export function addFriend() {
  const form = document.getElementById('addFriendForm');
  const usernameInput = document.getElementById('usernameInput');

  console.log(form);
  console.log(usernameInput);

  form.addEventListener('formValid', async () => {
    const friend = {
      username: usernameInput.value,
    };

    const result = await friendsService.addFriend(friend);
    if (result) {
      await loadPage('/friends');
    }
  });
}
