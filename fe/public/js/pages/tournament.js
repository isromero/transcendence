import { profileService } from '../services/profile.js';
import { tournamentService } from '../services/tournaments.js';
import { showErrorToast, updateTournamentUI } from '../utils/helpers.js';
import { loadPage } from '../router/router.js';
import { initGame } from '../game.js';

function getJoinCodeFromURL() {
  const urlParts = window.location.pathname.split('/');
  return urlParts[urlParts.length - 1];
}

const joinCode = getJoinCodeFromURL();
const startTournamentBtn = document.getElementById('start-tournament-btn');

function getUserMatch(tournament, currentUserId) {
  const match = Object.values(tournament.matches)
    .flat()
    .find(
      match =>
        match?.player1?.id === currentUserId ||
        match?.player2?.id === currentUserId
    );

  return match?.match_id;
}

startTournamentBtn.addEventListener('click', async function () {
  try {
    const tournament = await tournamentService.getTournament(joinCode);
    if (!tournament) {
      return;
    }

    if (tournament.current_players < tournament.max_players) {
      showErrorToast(
        `Cannot start tournament. Waiting for more players. Current: ${tournament.current_players}/${tournament.max_players}`
      );
      return;
    }

    const tournamentId = tournament.id;
    const tournamentAfterStarting =
      await tournamentService.updateTournamentWhenStarting(tournamentId);
    if (!tournamentAfterStarting) {
      return;
    }
  } catch (error) {
    showErrorToast(
      `An error occurred while starting the tournament. ${error.message}`
    );
  }
});

const intervalId = setInterval(async () => {
  const tournament = await tournamentService.getTournament(joinCode);
  updateTournamentUI(tournament);
  if (tournament.status === 'ready') {
    startTournamentBtn.disabled = false;
  } else if (tournament.status === 'in_progress') {
    clearInterval(intervalId);

    const profile = await profileService.getProfile();
    if (!profile) {
      return;
    }

    const currentUserId = profile.data.id;

    console.log(currentUserId);
    console.log(tournament);
    console.log(getUserMatch(tournament, currentUserId));

    const userMatchId = getUserMatch(tournament, currentUserId);
    if (!userMatchId) {
      showErrorToast('No match found for your user.');
      return;
    }

    await loadPage(`/game/${userMatchId}`);
    await initGame();
  }
}, 1000);

window.addEventListener('beforeunload', () => {
  clearInterval(intervalId);
});

if (
  document.readyState !== 'loading' &&
  window.location.pathname.includes('/tournament/')
) {
  try {
    const tournament = await tournamentService.getTournament(joinCode);

    updateTournamentUI(tournament);
  } catch (error) {
    showErrorToast(`Error initializing the game: ${error}`);
  }
}
