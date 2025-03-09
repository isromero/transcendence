import { tournamentService } from '../services/tournaments.js';
import { showErrorToast, updateTournamentUI } from '../utils/helpers.js';
import { loadPage } from '../router/router.js';

async function joinTournament(username, joinCode) {
  try {
    const tournamentData = await tournamentService.getTournament(joinCode);

    if (!tournamentData) {
      return null;
    }

    const putResult = await tournamentService.updateTournamentWhenJoining(
      joinCode,
      tournamentData,
      username
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

  const username = document.getElementById('username').value.trim();
  const joinCode = document.getElementById('joinCode').value.trim();

  if (!username || !joinCode) {
    showErrorToast('Please fill in all fields.');
    return;
  }

  await joinTournament(username, joinCode);
});
