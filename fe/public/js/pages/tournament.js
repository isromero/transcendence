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
startTournamentBtn.addEventListener('click', async function () {
  try {
    const profile = await profileService.getProfile();
    if (!profile) {
      return;
    }

    const currentUserId = profile.data.id;

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

    // Search for the user's match
    let userMatchId = null;
    Object.values(tournamentAfterStarting.matches)
      .flat()
      .forEach(match => {
        if (
          match?.player1?.id === currentUserId ||
          match?.player2?.id === currentUserId
        ) {
          userMatchId = match.match_id;
        }
      });

    if (!userMatchId) {
      showErrorToast('No match found for your user.');
      return;
    }

    await loadPage(`/game/${userMatchId}`);
    await initGame();
  } catch (error) {
    showErrorToast(
      `An error occurred while starting the tournament. ${error.message}`
    );
  }
});

const intervalId = setInterval(async () => {
  const tournament = await tournamentService.getTournament(joinCode);
  updateTournamentUI(tournament);
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
