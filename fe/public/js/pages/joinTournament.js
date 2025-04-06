import { showErrorToast } from '../utils/helpers.js';
import { loadPage } from '../router/router.js';
import { tournamentService } from '../services/tournaments.js';
import { profileService } from '../services/profile.js';

export function init() {
  const form = document.getElementById('joinTournamentForm');

  async function handleFormSubmit(event) {
    event.preventDefault();

    const displayName = document.getElementById('displayName').value.trim();
    const joinCode = document.getElementById('joinCode').value.trim();

    if (!displayName || !joinCode) {
      showErrorToast('Please fill in all fields.');
      return;
    }

    await loadPage(`/tournament/${joinCode}`);

    const tournament = await tournamentService.getTournament(joinCode);
    if (!tournament) {
      showErrorToast('Tournament not found.');
      return;
    }

    const profile = await profileService.getProfile();
    if (!profile) {
      showErrorToast('Profile not found.');
      return;
    }

    await tournamentService.updateTournamentWhenJoining(
      joinCode,
      tournament,
      profile.data,
      displayName
    );
  }

  form?.addEventListener('submit', handleFormSubmit);

  return () => {
    form?.removeEventListener('submit', handleFormSubmit);
  };
}
