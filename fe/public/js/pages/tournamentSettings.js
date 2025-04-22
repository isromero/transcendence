import { loadPage } from '../router/router.js';
import { tournamentService } from '../services/tournaments.js';
import { profileService } from '../services/profile.js';
import { updateTournamentUI } from '../utils/helpers.js';
import { showErrorToast } from '../utils/helpers.js';

export function init() {
  const form = document.getElementById('tournamentSettingsForm');

  async function handleFormSubmit(event) {
    event.preventDefault();

    const tournamentName = document
      .getElementById('tournament-name')
      .value.trim();
    const displayName = document
      .getElementById('leader-display-name')
      .value.trim();

    const profile = await profileService.getProfile();
    if (!profile) {
      showErrorToast('Profile not found.');
      return;
    }

    const result = await tournamentService.createTournament(
      tournamentName,
      4,
      profile.data,
      displayName || profile.data.username // fallback if empty
    );

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
