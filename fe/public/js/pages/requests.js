import { friendsService } from '../services/friends.js';

const createRequestCard = request => `
  <article class="d-flex justify-content-between align-items-center border border-2 border-primary-color rounded p-3 mb-3">
    <div class="d-flex flex-column align-items-center" style="width: 40%">
      <img 
        class="rounded-circle mb-2" 
        alt="${request.username}'s avatar" 
        src="${request.avatar || '/images/default_avatar.webp'}"
        style="width: 80px; height: 80px; object-fit: cover"
      />
      <p class="text-principal-color button-text-size mb-0">
        ${request.username}
      </p>
    </div>
    <div class="d-flex flex-column align-items-end gap-2" style="width: 60%">
      <button 
        class="btn btn-success bs-primary text-success-color w-100"
        data-user-id="${request.id}"
        id="accept-request-btn"
      >
        Accept
      </button>
      <button 
        class="btn btn-danger bs-primary text-danger-color w-100"
        data-user-id="${request.id}"
        id="reject-request-btn"
      >
        Reject
      </button>
    </div>
  </article>
`;

export async function loadRequests() {
  const requests = await friendsService.getRequests();
  const requestsList = document.getElementById('requests-list');

  if (requests && requests.length > 0) {
    requestsList.innerHTML = requests
      .map(request => createRequestCard(request))
      .join('');
  } else {
    requestsList.innerHTML = `
      <div class="text-center text-principal-color p-4">
        <p data-translationKey="no-requests">No friend requests yet!</p>
      </div>
    `;
  }
}

document.addEventListener('click', async function (event) {
  const button = event.target.closest('button');
  if (!button) {
    return;
  }

  if (button.id === 'accept-request-btn') {
    const userId = button.dataset.userId;
    await friendsService.respondToRequest(userId, 'accept');
    await loadRequests();
  } else if (button.id === 'reject-request-btn') {
    const userId = button.dataset.userId;
    await friendsService.respondToRequest(userId, 'reject');
    await loadRequests();
  }
});

if (
  document.readyState !== 'loading' &&
  window.location.pathname.includes('/requests')
) {
  await loadRequests();
}
