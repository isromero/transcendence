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
  const nextRoundBtn = document.getElementById('next-round-btn');
  let intervalId = null;
  let isInitialized = false;
  let invalidTournament = false; // Flag to track invalid tournament codes

  const roundMap = {
    1: 'quarter_finals',
    2: 'semi_finals',
    3: 'finals',
  };

  async function leaveTournament() {
    clearInterval(intervalId);

    const tournament = await tournamentService.getTournament(joinCode);
    if (!tournament) {
      return;
    }

    await tournamentService.leaveTournament(joinCode, tournament.id);

    const updatedTournament = await tournamentService.getTournament(joinCode);

    if (updatedTournament.status === 'completed') {
      localStorage.setItem(
        'tournament_left',
        JSON.stringify({ joinCode, timestamp: Date.now() })
      );
      return; // Leave without deleting
    }

    const profile = await profileService.getProfile();
    const userId = profile?.data?.id;

    const noPlayersLeft = updatedTournament.current_players === 0;
    const onlyCurrentUserLeft =
      updatedTournament.current_players === 1 &&
      updatedTournament.players?.[0]?.id === userId;

    if (noPlayersLeft || onlyCurrentUserLeft) {
      await tournamentService.deleteTournament(joinCode, tournament.id);
    }

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

      const updatedTournament =
        await tournamentService.updateTournamentWhenStarting(tournament.id);
      if (updatedTournament) {
        updateTournamentUI(updatedTournament);
        await maybeRedirectToMatch(updatedTournament);
      }
    } catch (err) {
      showErrorToast(`Error starting tournament: ${err.message}`);
    }
  }

  async function handleLeaveTournament() {
    await leaveTournament();
    isInitialized = false;
    loadPage('/join-tournament');
  }

  async function initializeTournament() {
    if (isInitialized) {
      return;
    }

    try {
      const tournament = await tournamentService.getTournament(joinCode);
      if (!tournament) {
        throw Error('No tournament found.');
      }

      updateTournamentUI(tournament);

      const profile = await profileService.getProfile();
      if (profile && tournament.status === 'pending') {
        const playerAlreadyInTournament = tournament.players.some(
          player => player.id === profile.data.id
        );

        if (!playerAlreadyInTournament) {
          await tournamentService.updateTournamentWhenJoining(
            joinCode,
            tournament,
            profile.data
          );
        }
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

      isInitialized = true;
    } catch (error) {
      console.error('Initialization error:', error);
      showErrorToast(`Initialization error: ${error}`);
    }
  }

  async function maybeRedirectToMatch(tournament) {
    if (!tournament || tournament.status !== 'in_progress') {
      return;
    }

    const currentRoundKey = roundMap[tournament.current_round];
    const profile = await profileService.getProfile();

    if (!profile || !currentRoundKey) {
      return;
    }

    const userId = profile.data.id;
    const userMatch = tournament.matches[currentRoundKey]?.find(
      match => match.player1?.id === userId || match.player2?.id === userId
    );

    if (userMatch?.match_id && !userMatch.game_finished) {
      await loadPage(
        `/game/${userMatch.match_id}/tournament/${tournament.join_code}`
      );
    }
  }

  async function handleTournamentProgress() {
    try {
      if (invalidTournament) {
        clearInterval(intervalId); // Stop further requests if the tournament is invalid
        return;
      }

      const tournament = await tournamentService.getTournament(joinCode);
      if (!tournament) {
        invalidTournament = true; // Mark the tournament as invalid
        showErrorToast('Invalid tournament code. Please check and try again.');
        clearInterval(intervalId); // Stop further requests
        return;
      }

      updateTournamentUI(tournament);

      if (tournament.status === 'in_progress') {
        const currentRoundKey = roundMap[tournament.current_round];
        const currentRoundFinished =
          tournament.matches?.round_finished?.[currentRoundKey];

        const profile = await profileService.getProfile();
        const userId = profile?.data?.id;

        nextRoundBtn?.classList.add('hidden');
        nextRoundBtn?.setAttribute('disabled', 'true');

        if (currentRoundFinished && currentRoundKey && userId) {
          const completedRoundMatches =
            tournament.matches?.[currentRoundKey] || [];

          const winners = completedRoundMatches
            .map(match => {
              if (
                !match.player1?.id ||
                !match.player2?.id ||
                match.player1.score === undefined ||
                match.player2.score === undefined
              ) {
                return null;
              }
              return match.player1.score > match.player2.score
                ? match.player1.id
                : match.player2.id;
            })
            .filter(id => id !== null);

          if (winners.includes(userId)) {
            if (currentRoundKey !== 'finals') {
              nextRoundBtn?.classList.remove('hidden');
              nextRoundBtn?.removeAttribute('disabled');
            }
          }
        }

        await maybeRedirectToMatch(tournament);
      } else if (tournament.status === 'ready') {
        const profile = await profileService.getProfile();
        const playerId = Number(profile?.data?.id);
        const leaderId = Number(tournament.players?.[0]?.id);

        if (playerId === leaderId) {
          startBtn?.removeAttribute('disabled');
        }
      } else if (tournament.status === 'pending') {
        startBtn?.setAttribute('disabled', 'true');
      } else if (tournament.status === 'completed') {
        leaveBtn?.classList.remove('hidden');
        startBtn?.classList.add('hidden');
        nextRoundBtn?.classList.add('hidden');
        nextRoundBtn?.setAttribute('disabled', 'true');
      }
    } catch (error) {
      console.error('Error in handleTournamentProgress:', error);
      showErrorToast(`Error in tournament progress: ${error.message}`);
      clearInterval(intervalId); // Stop further requests on error
    }
  }

  intervalId = setInterval(handleTournamentProgress, 1000);

  nextRoundBtn?.addEventListener('click', async () => {
    try {
      const tournament = await tournamentService.getTournament(joinCode);
      if (!tournament) {
        return;
      }

      // Go to the next round
      const updatedTournament = await tournamentService.goToNextRound(
        tournament.id
      );
      if (updatedTournament) {
        // Update the UI and redirect to the next round matches
        updateTournamentUI(updatedTournament);
        await maybeRedirectToMatch(updatedTournament);
      }
    } catch (error) {
      showErrorToast(`Error going to next round: ${error.message}`);
    }
  });
  startBtn?.addEventListener('click', handleStartTournament);
  leaveBtn?.addEventListener('click', handleLeaveTournament);
  window.addEventListener('storage', handleStorageChange);

  initializeTournament();

  // If you leave the tournament with popstate and beforeunload / others
  // We don't care, we won't do anything
  // We only care if you leave the tournament with the leave button
  // This is because it's a little buggy if we handle that way

  return () => {
    clearInterval(intervalId);
    startBtn?.removeEventListener('click', handleStartTournament);
    leaveBtn?.removeEventListener('click', handleLeaveTournament);
    window.removeEventListener('storage', handleStorageChange);
    isInitialized = false;
  };
}
