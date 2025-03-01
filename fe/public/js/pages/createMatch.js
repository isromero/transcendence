import { loadPage } from '../router/router.js';
import { showErrorToast } from '../utils/helpers.js';
import { historyService } from '../services/history.js';

document.addEventListener('click', async function (event) {
  if (event.target && event.target.id === 'local-match-btn') {
    event.preventDefault();
    try {
      const data = await historyService.createMatch();
      if (!data || !data.match_id) {
        return;
      }

      loadPage(`/game/${data.match_id}`);
    } catch (error) {
      showErrorToast(`Error creating match: ${error}. Please try again.`);
    }
  }
});
