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

    try {
      
      const tournament = await tournamentService.getTournament(joinCode);
      if (!tournament) {
        showErrorToast('Tournament not found. Please check the code and try again.');
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

      
      await loadPage(`/tournament/${joinCode}`);
    } catch (error) {
      console.error('Error joining tournament:', error);
      showErrorToast('An error occurred while joining the tournament.');
    }
  }

  form?.addEventListener('submit', handleFormSubmit);

  return () => {
    form?.removeEventListener('submit', handleFormSubmit);
  };
}
