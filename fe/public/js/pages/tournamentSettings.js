import { loadPage } from '../router/router.js';
import { tournamentService } from '../services/tournaments.js';
import { updateTournamentUI } from '../utils/helpers.js';

export function init() {
  const form = document.getElementById('tournamentSettingsForm');
  let lastClickedButton = null;

  async function handleFormSubmit(event) {
    event.preventDefault();

    const tournamentName = document.getElementById('tournament-name').value;

    if (lastClickedButton?.id === '4-players-btn') {
      const result = await tournamentService.createTournament(
        tournamentName,
        4
      );
      if (result) {
        await loadPage(`/tournament/${result.join_code}`);
        await updateTournamentUI(result);
      }
    } else if (lastClickedButton?.id === '8-players-btn') {
      const result = await tournamentService.createTournament(
        tournamentName,
        8
      );
      if (result) {
        await loadPage(`/tournament/${result.join_code}`);
        await updateTournamentUI(result);
      }
    }
  }

  function handleButtonClick(event) {
    if (event.target.type === 'submit') {
      lastClickedButton = event.target;
    }
  }

  form?.addEventListener('click', handleButtonClick);
  form?.addEventListener('formValid', handleFormSubmit);

  return () => {
    form?.removeEventListener('click', handleButtonClick);
    form?.removeEventListener('formValid', handleFormSubmit);
  };
}
