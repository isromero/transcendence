import { loadPage } from '../router/router.js';
import { tournamentService } from '../services/tournaments.js';
import { updateTournamentUI } from '../utils/helpers.js';

export function init() {
  const form = document.getElementById('tournamentSettingsForm');

  async function handleFormSubmit(event) {
    event.preventDefault();

    const tournamentName = document.getElementById('tournament-name').value;

    const result = await tournamentService.createTournament(tournamentName, 4);
    if (result) {
      await loadPage(`/tournament/${result.join_code}`);
      await updateTournamentUI(result);
    }
  }

  form?.addEventListener('formValid', handleFormSubmit);

  return () => {
    form?.removeEventListener('formValid', handleFormSubmit);
  };
}
