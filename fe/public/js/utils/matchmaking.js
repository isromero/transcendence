import { loadPage } from '../router/router.js';
import { showErrorToast } from './helpers.js';

let ws;
let multiplayerBtn;
let queueStatus;
let localMatchBtn;
let cancelQueueBtn;
let tournamentBtn;

export function initMatchmaking() {
  multiplayerBtn = document.getElementById('multiplayer-btn');
  queueStatus = document.getElementById('queue-status');
  localMatchBtn = document.getElementById('local-match-btn');
  cancelQueueBtn = document.getElementById('cancel-queue-btn');
  tournamentBtn = document.getElementById('tournament-btn');

  handleQueue();

  cancelQueueBtn.addEventListener('click', cleanupMatchmaking);
  window.addEventListener('popstate', cleanupMatchmaking);
  window.addEventListener('beforeunload', cleanupMatchmaking);
}

function handleQueue() {
  queueStatus.style.display = 'block';
  localMatchBtn.style.display = 'none';
  multiplayerBtn.style.display = 'none';
  tournamentBtn.style.display = 'none';

  ws = new WebSocket(`wss://${window.location.hostname}:8443/ws/matchmaking`);

  ws.onmessage = async event => {
    const data = JSON.parse(event.data);

    if (data.type === 'start_match') {
      await loadPage(`/game/${data.match_id}`);
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
    ws.close();
    ws = null;
  }

  queueStatus.style.display = 'none';
  localMatchBtn.style.display = 'block';
  multiplayerBtn.style.display = 'block';
  tournamentBtn.style.display = 'block';
}
