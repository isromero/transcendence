import { loadPage } from '../router/router.js';
import { showErrorToast } from '../utils/helpers.js';
import { historyService } from '../services/history.js';
import { initMatchmaking } from '../utils/matchmaking.js';

export function init() {
  async function handleLocalMatch() {
    try {
      const data = await historyService.createMatch();
      if (!data || !data.match_id) {
        return;
      }

      await loadPage(`/game/${data.match_id}`);
    } catch (error) {
      showErrorToast(`Error creating match: ${error}. Please try again.`);
    }
  }

  function handleMultiplayer() {
    try {
      initMatchmaking();
    } catch (error) {
      showErrorToast(`Error creating matchmaking: ${error}. Please try again.`);
    }
  }

  async function handleClick(event) {
    event.preventDefault();
    const target = event.target;

    if (target.id === 'local-match-btn') {
      await handleLocalMatch();
    } else if (target.id === 'multiplayer-btn') {
      handleMultiplayer();
    }
  }

  document.addEventListener('click', handleClick);

  return () => {
    document.removeEventListener('click', handleClick);
  };
}
