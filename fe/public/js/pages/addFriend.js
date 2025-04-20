import { loadPage } from '../router/router.js';
import { friendsService } from '../services/friends.js';

export function init() {
  const form = document.getElementById('addFriendForm');
  const usernameInput = document.getElementById('usernameInput');

  async function handleFormSubmit() {
    const friend = {
      username: usernameInput.value,
    };

    const result = await friendsService.addFriend(friend);
    if (result) {
      await loadPage('/friends', { updateHistory: false });
    }
  }

  form?.addEventListener('formValid', handleFormSubmit);

  return () => {
    form?.removeEventListener('formValid', handleFormSubmit);
  };
}
