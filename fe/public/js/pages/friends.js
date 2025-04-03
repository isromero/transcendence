import { friendsService } from '../services/friends.js';
import { IMAGES_URL } from '../utils/constants.js';

function createFriendCard(friend) {
  return `
    <a class="spa-link" href="/profile/${friend.id}">
      <article class="d-flex justify-content-between align-items-center border border-2 border-primary-color rounded p-2 mb-2">
        <div class="d-flex flex-column align-items-center" style="max-width: 80px; flex: 1 0 20vw;">
          <img 
            class="rounded-circle mb-1" 
            alt="${friend.username}'s avatar" 
            src="${friend.avatar ? `${IMAGES_URL}${friend.avatar.replace('/images/', '/')}` : `${IMAGES_URL}/default_avatar.webp`}"
            style="width: 60px; height: 60px; object-fit: cover"
          />
          <p class="text-principal-color small mb-0 text-truncate">
            ${friend.username}
          </p>
        </div>
        <div class="d-flex flex-column align-items-end" style="flex: 2 0 60%;">
          <div class="d-flex align-items-center mb-1">
            <span class="text-${friend.is_online ? 'success' : 'secondary'} me-1" style="font-size: 0.6rem;">●</span>
            <span class="text-principal-color small">${friend.is_online ? 'Online' : 'Offline'}</span>
          </div>
          <p class="text-principal-color small mb-1">
            <span data-translationKey="wins" class="me-1">Wins</span>: <span>${friend.wins || 0}</span>
          </p>
          <p class="text-principal-color small mb-1">
            <span data-translationKey="loses" class="me-1">Loses</span>: <span>${friend.loses || 0}</span>
          </p>
          <p class="text-principal-color small mb-0">
            <span data-translationKey="total" class="me-1">Total</span>: <span>${(friend.wins || 0) + (friend.loses || 0)}</span>
          </p>
        </div>
      </article>
    </a>
  `;
}

export function init() {
  const friendsList = document.getElementById('friends-list');

  async function loadFriends() {
    const friends = await friendsService.getFriends();

    if (friends && friends.length > 0) {
      friendsList.innerHTML = friends
        .map(friend => createFriendCard(friend))
        .join('');
    } else {
      friendsList.innerHTML = `
        <div class="text-center text-principal-color p-2">
          <p data-translationKey="no-friends" class="small">No friends yet. Add some friends to play with!</p>
        </div>
      `;
    }
  }

  loadFriends();

  return () => {};
}
