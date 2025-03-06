import { loadPage } from '../router/router.js';
import { showErrorToast } from '../utils/helpers.js';
import { historyService } from '../services/history.js';
import { initGame } from '../game.js';
import { initMatchmaking } from '../matchmaking.js';

document.addEventListener('click', async function (event) {
  event.preventDefault();
  if (event.target && event.target.id === 'local-match-btn') {
    try {
      const data = await historyService.createMatch();
      if (!data || !data.match_id) {
        return;
      }

      await loadPage(`/game/${data.match_id}`);
      await initGame();
    } catch (error) {
      showErrorToast(`Error creating match: ${error}. Please try again.`);
    }
  }
  if (event.target && event.target.id === 'multiplayer-btn') {
    try {
      initMatchmaking();
    } catch (error) {
      showErrorToast(`Error creating matchmaking: ${error}. Please try again.`);
    }
  }
});