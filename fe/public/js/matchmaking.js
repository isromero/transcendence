import { loadPage } from './router/router.js';
import { initGame } from './game.js';
import { showErrorToast } from './utils/helpers.js';

let ws;
let multiplayerBtn;
let queueStatus;
let localMatchBtn;
let cancelQueueBtn;

export function initMatchmaking() {
  multiplayerBtn = document.getElementById('multiplayer-btn');
  queueStatus = document.getElementById('queue-status');
  localMatchBtn = document.getElementById('local-match-btn');
  cancelQueueBtn = document.getElementById('cancel-queue-btn');

  if (sessionStorage.getItem('matchmaking_active')) {
    showErrorToast('You are already in a matchmaking.');
    return;
  }

  handleQueue();

  cancelQueueBtn.addEventListener('click', cleanupMatchmaking);
  window.addEventListener('popstate', cleanupMatchmaking);
  window.addEventListener('beforeunload', cleanupMatchmaking);
}

function handleQueue() {
  if (ws) {
    // If there is a WebSocket, close it
    ws.close();
    ws = null;
  }

  // Display the queue status
  queueStatus.style.display = 'block';
  // Hide the buttons
  localMatchBtn.style.display = 'none';
  multiplayerBtn.style.display = 'none';

  sessionStorage.setItem('matchmaking_active', 'true');

  ws = new WebSocket((`ws://${window.location.hostname}:8000/ws/game/matchmaking`));

  ws.onmessage = async event => {
    const data = JSON.parse(event.data);

    if (data.type === 'start_match') {
      sessionStorage.removeItem('matchmaking_active');
      sessionStorage.setItem('player_role', data.player);

      await loadPage(`/game/${data.match_id}`);
      await initGame();
    } else if (data.type === 'error') {
      showErrorToast('Error starting matchmaking.');
      cleanupMatchmaking();
    }
  };

  ws.onclose = () => {
    cleanupMatchmaking();
  };

  ws.onerror = () => {
    cleanupMatchmaking();
  };
}

function cleanupMatchmaking() {
  cancelQueueBtn.removeEventListener('click', cleanupMatchmaking);
  window.removeEventListener('popstate', cleanupMatchmaking);
  window.removeEventListener('beforeunload', cleanupMatchmaking);

  if (ws) {
    // If there is a WebSocket, close it
    ws.close();
    ws = null;
  }
  sessionStorage.removeItem('matchmaking_active');

  queueStatus.style.display = 'none';
  localMatchBtn.style.display = 'block';
  multiplayerBtn.style.display = 'block';
}
