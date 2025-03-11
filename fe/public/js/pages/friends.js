import { addFriend } from './addFriend.js';

document.addEventListener('click', event => {
  event.preventDefault();

  const target = event.target;

  if (target.matches('#newFriendButton')) {
    document.addEventListener('spaContentLoaded', () => addFriend(), {
      once: true,
    });
  }
});
