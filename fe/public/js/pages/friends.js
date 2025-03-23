import { friendsService } from '../services/friends.js';
import { IMAGES_URL } from '../utils/constants.js';
const createFriendCard = friend => `
<a class="spa-link" href="/profile/${friend.id}">
  <article class="d-flex justify-content-between align-items-center border border-2 border-primary-color rounded p-3 mb-3">
    <div class="d-flex flex-column align-items-center" style="width: 40%">
      <img 
        class="rounded-circle mb-2" 
        alt="${friend.username}'s avatar" 
        src="${friend.avatar ? `${IMAGES_URL}${friend.avatar.replace('/images/', '/')}` : `${IMAGES_URL}/default_avatar.webp`}"
        style="width: 80px; height: 80px; object-fit: cover"
      />
      <p class="text-principal-color button-text-size mb-0">
        ${friend.username}
      </p>
    </div>
    <div class="d-flex flex-column align-items-end" style="width: 60%">
      <div class="d-flex align-items-center mb-2">
        <span class="text-${friend.is_online ? 'success' : 'secondary'} me-2">●</span>
        <span class="text-principal-color">${friend.is_online ? 'Online' : 'Offline'}</span>
      </div>
      <p class="text-principal-color button-text-size mb-1">
        <span data-translationKey="wins">Wins</span>: <span>${friend.wins || 0}</span>
      </p>
      <p class="text-principal-color button-text-size mb-1">
        <span data-translationKey="loses">Loses</span>: <span>${friend.loses || 0}</span>
      </p>
      <p class="text-principal-color button-text-size mb-0">
        <span data-translationKey="total">Total</span>: <span>${(friend.wins || 0) + (friend.loses || 0)}</span>
      </p>
    </div>
  </article>
</a>
`;

export const loadFriends = async () => {
  const friends = await friendsService.getFriends();

  const friendsList = document.getElementById('friends-list');

  if (friends && friends.length > 0) {
    friendsList.innerHTML = friends
      .map(friend => createFriendCard(friend))
      .join('');
  } else {
    friendsList.innerHTML = `
        <div class="text-center text-principal-color p-4">
          <p data-translationKey="no-friends">No friends yet. Add some friends to play with!</p>
        </div>
      `;
  }
};

if (
  document.readyState !== 'loading' &&
  window.location.pathname.includes('/friends')
) {
  await loadFriends();
}
