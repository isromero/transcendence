import { profileService } from '../services/profile.js';
import { tournamentService } from '../services/tournaments.js';
import { showErrorToast, updateTournamentUI } from '../utils/helpers.js';
import { loadPage } from '../router/router.js';

function getJoinCodeFromURL() {
  const urlParts = window.location.pathname.split('/');
  const joinCode = urlParts[urlParts.length - 1];
  console.log('🔍 Código del torneo extraído de la URL:', joinCode);
  return joinCode;
}

function getUserMatch(tournament, currentUserId) {
  console.log('🔎 Buscando el match del usuario en el torneo...', {
    tournament,
    currentUserId,
  });

  const match = Object.values(tournament.matches)
    .flat()
    .find(
      match =>
        match?.player1?.id === currentUserId ||
        match?.player2?.id === currentUserId
    );

  console.log('🎯 Match encontrado para el usuario:', match);
  return match?.match_id;
}

export function init() {
  const joinCode = getJoinCodeFromURL();
  const startBtn = document.getElementById('start-tournament-btn');
  const leaveBtn = document.getElementById('leaveTournamentButton');
  let intervalId;

  if (!startBtn) {
    console.error('❌ Botón de inicio no encontrado.');
  }

  async function leaveTournament() {
    console.log('🚪 Saliendo del torneo...');
    clearInterval(intervalId);

    const tournament = await tournamentService.getTournament(joinCode);
    if (!tournament) {
      console.error('❌ Error obteniendo el torneo al salir.');
      return;
    }

    await tournamentService.leaveTournament(joinCode, tournament.id);

    // Notificar en localStorage para otros tabs
    localStorage.setItem(
      'tournament_left',
      JSON.stringify({ joinCode, timestamp: Date.now() })
    );

    console.log('👋 Salida completada.');
  }

  function handleStorageChange(event) {
    if (event.key === 'tournament_left') {
      const data = JSON.parse(event.newValue);
      if (data.joinCode === joinCode) {
        console.log('🔄 Otro tab salió del torneo. Redirigiendo...');
        loadPage('/join-tournament');
      }
    }
  }

  async function handleStartTournament() {
    try {
      const tournament = await tournamentService.getTournament(joinCode);
      if (!tournament) return;

      if (tournament.current_players < tournament.max_players) {
        showErrorToast(
          `Waiting for more players: ${tournament.current_players}/${tournament.max_players}`
        );
        return;
      }

      await tournamentService.updateTournamentWhenStarting(tournament.id);
    } catch (err) {
      console.error('❌ Error al iniciar torneo:', err);
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
      if (!tournament) throw Error('No tournament found.');

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
      console.error('🔥 Error al inicializar:', error);
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

    if (!profile || !currentRoundKey) return;

    const userId = profile.data.id;

    const userMatch = tournament.matches[currentRoundKey]?.find(
      match =>
        !match.game_finished &&
        (match.player1?.id === userId || match.player2?.id === userId)
    );

    if (userMatch?.match_id) {
      console.log(`🎮 Redirigiendo a tu match (${currentRoundKey})`);
      await loadPage(`/game/${userMatch.match_id}/tournament/${tournament.join_code}`);
    } else {
      console.log(`🧘 No hay match activo para ti en ${currentRoundKey}`);
    }
  }

  async function handleTournamentProgress() {
    const tournament = await tournamentService.getTournament(joinCode);
    if (!tournament) return;

    const tournamentpolita = await tournamentService.getTournament(joinCode);
    console.log('📊 Estado del torneo actualizado:', tournamentpolita);

    updateTournamentUI(tournament);

    if (tournament.status === 'in_progress') {
      const roundMap = {
        1: 'quarter_finals',
        2: 'semi_finals',
        3: 'finals',
      };
      const currentRoundKey = roundMap[tournament.current_round];
      const currentRoundFinished = tournament.matches.round_finished?.[currentRoundKey];

      if (currentRoundFinished) {
        console.log(`📢 Ronda ${currentRoundKey} finalizada. Avanzando...`);
        const result = await tournamentService.goToNextRound(tournament.id);

        if (!result) {
          console.error('❌ No se pudo avanzar ronda.');
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

  // Interval para monitorear el estado del torneo
  intervalId = setInterval(handleTournamentProgress, 1000);

  // Listeners
  startBtn?.addEventListener('click', handleStartTournament);
  leaveBtn?.addEventListener('click', handleLeaveTournament);
  window.addEventListener('beforeunload', handleBeforeUnload);
  window.addEventListener('storage', handleStorageChange);

  initializeTournament();

  // Cleanup
  return () => {
    clearInterval(intervalId);
    startBtn?.removeEventListener('click', handleStartTournament);
    leaveBtn?.removeEventListener('click', handleLeaveTournament);
    window.removeEventListener('beforeunload', handleBeforeUnload);
    window.removeEventListener('storage', handleStorageChange);
    leaveTournament();
  };
}

