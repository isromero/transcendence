import { profileService } from '../services/profile.js';
import { tournamentService } from '../services/tournaments.js';
import { showErrorToast, updateTournamentUI } from '../utils/helpers.js';
import { loadPage } from '../router/router.js';

function getJoinCodeFromURL() {
  const urlParts = window.location.pathname.split('/');
  const joinCode = urlParts[urlParts.length - 1];
  return joinCode;
}

export function init() {
  const joinCode = getJoinCodeFromURL();
  const startBtn = document.getElementById('start-tournament-btn');
  const leaveBtn = document.getElementById('leaveTournamentButton');
  let intervalId = null;

  async function leaveTournament() {
    clearInterval(intervalId);

    const tournament = await tournamentService.getTournament(joinCode);
    if (!tournament) {
      return;
    }

    await tournamentService.leaveTournament(joinCode, tournament.id);

    localStorage.setItem(
      'tournament_left',
      JSON.stringify({ joinCode, timestamp: Date.now() })
    );
  }

  function handleStorageChange(event) {
    if (event.key === 'tournament_left') {
      const data = JSON.parse(event.newValue);
      if (data.joinCode === joinCode) {
        loadPage('/join-tournament');
      }
    }
  }

  async function handleStartTournament() {
    try {
      const tournament = await tournamentService.getTournament(joinCode);
      if (!tournament) {
        return;
      }

      if (tournament.current_players < tournament.max_players) {
        showErrorToast(
          `Waiting for more players: ${tournament.current_players}/${tournament.max_players}`
        );
        return;
      }

      await tournamentService.updateTournamentWhenStarting(tournament.id);
    } catch (err) {
      showErrorToast(`Error starting tournament: ${err.message}`);
    }
  }

  async function handleLeaveTournament() {
    await leaveTournament();
    loadPage('/join-tournament');
  }

  async function handleBeforeUnload(event) {
    event.preventDefault();
    event.returnValue = '';
    await leaveTournament();
  }

  async function initializeTournament() {
    try {
      const tournament = await tournamentService.getTournament(joinCode);
      if (!tournament) {
        throw Error('No tournament found.');
      }

      updateTournamentUI(tournament);

      const profile = await profileService.getProfile();
      if (profile) {
        await tournamentService.updateTournamentWhenJoining(
          joinCode,
          tournament,
          profile.username
        );
      }

      if (tournament.status === 'in_progress') {
        leaveBtn?.classList.add('hidden');
        startBtn?.classList.add('hidden');
        await maybeRedirectToMatch(tournament);
      }
      if (tournament.status === 'completed') {
        leaveBtn?.classList.remove('hidden');
        startBtn?.classList.add('hidden');
      }
    } catch (error) {
      showErrorToast(`Initialization error: ${error}`);
    }
  }

  async function maybeRedirectToMatch(tournament) {
    const roundMap = {
      1: 'quarter_finals',
      2: 'semi_finals',
      3: 'finals',
    };
    const currentRoundKey = roundMap[tournament.current_round];
    const profile = await profileService.getProfile();

    if (!profile || !currentRoundKey) {
      return;
    }

    const userId = profile.data.id;

    const userMatch = tournament.matches[currentRoundKey]?.find(
      match =>
        !match.game_finished &&
        (match.player1?.id === userId || match.player2?.id === userId)
    );

    if (userMatch?.match_id) {
      await loadPage(
        `/game/${userMatch.match_id}/tournament/${tournament.join_code}`
      );
    } else {
      console.error('No match found for user in current round');
    }
  }

  async function handleTournamentProgress() {
    const tournament = await tournamentService.getTournament(joinCode);
    if (!tournament) {
      return;
    }

    updateTournamentUI(tournament);

    if (tournament.status === 'in_progress') {
      const roundMap = {
        1: 'quarter_finals',
        2: 'semi_finals',
        3: 'finals',
      };
      const currentRoundKey = roundMap[tournament.current_round];
      const currentRoundFinished =
        tournament.matches.round_finished?.[currentRoundKey];

      if (currentRoundFinished) {
        const result = await tournamentService.goToNextRound(tournament.id);

        if (!result) {
          return;
        }

        await maybeRedirectToMatch(result);
        return;
      }

      await maybeRedirectToMatch(tournament);
    } else if (tournament.status === 'ready') {
      const profile = await profileService.getProfile();
      const playerId = Number(profile?.data?.id);
      const leaderId = Number(tournament.players?.[0]?.id);

      if (playerId === leaderId) {
        startBtn?.removeAttribute('disabled');
      }
    }
  }

  intervalId = setInterval(handleTournamentProgress, 1000);

  startBtn?.addEventListener('click', handleStartTournament);
  leaveBtn?.addEventListener('click', handleLeaveTournament);
  window.addEventListener('beforeunload', handleBeforeUnload);
  window.addEventListener('storage', handleStorageChange);

  initializeTournament();

  return () => {
    clearInterval(intervalId);
    startBtn?.removeEventListener('click', handleStartTournament);
    leaveBtn?.removeEventListener('click', handleLeaveTournament);
    window.removeEventListener('beforeunload', handleBeforeUnload);
    window.removeEventListener('storage', handleStorageChange);
    leaveTournament();
  };
}
