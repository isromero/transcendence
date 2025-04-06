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

  // Check if there is a queue active in any tab
  const isInQueue = localStorage.getItem('matchmaking_active');
  if (isInQueue) {
    showErrorToast('You are already in a matchmaking queue in another tab.');
    return;
  }

  handleQueue();

  window.addEventListener('storage', handleStorageChange);
  cancelQueueBtn.addEventListener('click', cleanupMatchmaking);
  window.addEventListener('popstate', cleanupMatchmaking);
  window.addEventListener('beforeunload', cleanupMatchmaking);
}

function handleStorageChange(event) {
  if (event.key === 'matchmaking_active') {
    if (event.newValue === null && ws) {
      // If the queue was cancelled in another tab, clean this one also
      cleanupMatchmaking();
    }
  }
}

function handleQueue() {
  queueStatus.style.display = 'block';
  localMatchBtn.style.display = 'none';
  multiplayerBtn.style.display = 'none';
  tournamentBtn.style.display = 'none';

  localStorage.setItem('matchmaking_active', 'true');

  ws = new WebSocket(`ws://${window.location.hostname}:8000/ws/matchmaking`);

  ws.onmessage = async event => {
    const data = JSON.parse(event.data);

    if (data.type === 'start_match') {
      localStorage.removeItem('matchmaking_active');
      sessionStorage.setItem('player_role', data.player);
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
  window.removeEventListener('storage', handleStorageChange);

  if (ws) {
    ws.close();
    ws = null;
  }
  localStorage.removeItem('matchmaking_active');

  queueStatus.style.display = 'none';
  localMatchBtn.style.display = 'block';
  multiplayerBtn.style.display = 'block';
  tournamentBtn.style.display = 'block';
}
