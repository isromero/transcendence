import { tournamentService } from '../services/tournaments.js';
import { showErrorToast, updateTournamentUI } from '../utils/helpers.js';
import { loadPage } from '../router/router.js';

export async function joinTournament(displayName, joinCode) {
  try {
    const tournamentData = await tournamentService.getTournament(joinCode);

    if (!tournamentData) {
      return null;
    }

    const putResult = await tournamentService.updateTournamentWhenJoining(
      joinCode,
      tournamentData,
      displayName
    );

    if (!putResult) {
      return null;
    }

    await loadPage(`/tournament/${joinCode}`);

    updateTournamentUI(tournamentData);
  } catch (error) {
    showErrorToast(
      `An error occurred while joining the tournament. ${error.message}`
    );
    return null;
  }
}

const joinTournamentForm = document.getElementById('joinTournamentForm');

joinTournamentForm.addEventListener('submit', async function (event) {
  event.preventDefault();

  const displayName = document.getElementById('displayName').value.trim();
  const joinCode = document.getElementById('joinCode').value.trim();

  if (!displayName || !joinCode) {
    showErrorToast('Please fill in all fields.');
    return;
  }

  await joinTournament(displayName, joinCode);
});
