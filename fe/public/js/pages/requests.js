import { friendsService } from '../services/friends.js';
import { IMAGES_URL } from '../utils/constants.js';

function createRequestCard(request) {
  return `
    <article class="d-flex flex-column flex-md-row justify-content-between align-items-center border border-2 border-primary-color rounded p-3 mb-3">
      <div class="d-flex flex-column align-items-center col-12 col-md-4">
        <img 
          class="rounded-circle mb-2" 
          alt="${request.username}'s avatar" 
          src="${request.avatar ? `${IMAGES_URL}${request.avatar.replace('/images/', '/')}` : `${IMAGES_URL}/default_avatar.webp`}"
          style="width: 80px; height: 80px; object-fit: cover"
        />
        <p class="text-principal-color button-text-size mb-0 text-center text-md-start">
          ${request.username}
        </p>
      </div>
      <div class="d-flex flex-column align-items-center align-items-md-end gap-2 col-12 col-md-6 mt-2 mt-md-0">
        <button 
          class="btn btn-success bs-primary text-success-color w-100 w-md-auto"
          data-user-id="${request.id}"
          id="accept-request-btn"
        >
          Accept
        </button>
        <button 
          class="btn btn-danger bs-primary text-danger-color w-100 w-md-auto"
          data-user-id="${request.id}"
          id="reject-request-btn"
        >
          Reject
        </button>
      </div>
    </article>
  `;
}

export function init() {
  const requestsList = document.getElementById('requests-list');

  async function loadRequests() {
    const requests = await friendsService.getRequests();

    if (requests && requests.length > 0) {
      requestsList.innerHTML = requests
        .map(request => createRequestCard(request))
        .join('');
    } else {
      let langu = document.documentElement.lang;

      if (langu === 'uk-UA') {
        langu = 'Ще немає запитів на дружбу!';
      } else if (langu === 'en') {
        langu = 'No friend requests yet!';
      } else {
        langu = '¡Aún no tienes solicitudes de amistad!';
      }
      requestsList.innerHTML = `
        <div class="text-center text-principal-color p-4">
          <p>${langu}</p>
        </div>
      `;
    }
  }

  async function handleRequestAction(event) {
    const button = event.target.closest('button');
    if (!button) {
      return;
    }

    const userId = button.dataset.userId;

    if (button.id === 'accept-request-btn') {
      await friendsService.respondToRequest(userId, 'accept');
      await loadRequests();
    } else if (button.id === 'reject-request-btn') {
      await friendsService.respondToRequest(userId, 'reject');
      await loadRequests();
    }
  }

  loadRequests();

  document.addEventListener('click', handleRequestAction);

  return () => {
    document.removeEventListener('click', handleRequestAction);
  };
}
