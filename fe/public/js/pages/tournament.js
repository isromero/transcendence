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
  const startTournamentBtn = document.getElementById('start-tournament-btn');
  const leaveTournamentButton = document.getElementById(
    'leaveTournamentButton'
  );
  let intervalId;

  if (!startTournamentBtn) {
    console.error('❌ Error: No se encontró el botón de inicio en el DOM.');
  }

  async function leaveTournament() {
    console.log('🚪 Saliendo del torneo...');
    clearInterval(intervalId);

    const tournament = await tournamentService.getTournament(joinCode);
    console.log('📌 Datos del torneo al salir:', tournament);

    if (!tournament) {
      console.error(
        '❌ Error: No se pudo obtener el torneo al intentar salir.'
      );
      throw Error('Get Tournament failed');
    }

    await tournamentService.leaveTournament(joinCode, tournament.id);
    // Notify other tabs
    localStorage.setItem(
      'tournament_left',
      JSON.stringify({
        joinCode,
        timestamp: Date.now(),
      })
    );
    console.log('👋 Salida del torneo completada.');
  }

  async function handleStartTournament() {
    try {
      console.log('🚀 Intentando iniciar el torneo...');

      const tournament = await tournamentService.getTournament(joinCode);
      console.log('📌 Datos del torneo al intentar iniciar:', tournament);

      if (!tournament) {
        console.error('❌ No se pudo obtener el torneo.');
        return;
      }

      if (tournament.current_players < tournament.max_players) {
        console.warn(
          `⚠️ No hay suficientes jugadores: ${tournament.current_players}/${tournament.max_players}`
        );
        showErrorToast(
          `Cannot start tournament. Waiting for more players. Current: ${tournament.current_players}/${tournament.max_players}`
        );
        return;
      }

      console.log('✅ Suficientes jugadores, iniciando torneo...');
      const tournamentId = tournament.id;
      const tournamentAfterStarting =
        await tournamentService.updateTournamentWhenStarting(tournamentId);

      console.log('🏁 Torneo después de iniciar:', tournamentAfterStarting);

      if (!tournamentAfterStarting) {
        console.error('❌ Error al actualizar el torneo después de iniciar.');
        return;
      }
    } catch (error) {
      console.error('🔥 Error inesperado al iniciar el torneo:', error);
      showErrorToast(
        `An error occurred while starting the tournament. ${error.message}`
      );
    }
  }

  async function handleLeaveTournament() {
    console.log('🛑 Botón de salir presionado. Saliendo del torneo...');
    await leaveTournament();
    loadPage('/join-tournament');
  }

  async function handlePopState() {
    console.log('🔄 Popstate event triggered.');
    await leaveTournament();
    loadPage('/');
  }

  async function handleBeforeUnload(event) {
    console.log('⚠️ Evento beforeunload detectado. Saliendo del torneo...');
    event.preventDefault();
    event.returnValue = ''; // Necessary for some browsers
    await leaveTournament();
  }

  // Handle storage events to detect changes in other tabs
  function handleStorageChange(event) {
    if (event.key === 'tournament_left') {
      const data = JSON.parse(event.newValue);
      if (data.joinCode === joinCode) {
        console.log('🔄 User has left the tournament in another tab');
        loadPage('/join-tournament');
      }
    }
  }

  async function initializeTournament() {
    try {
      console.log('📥 Página cargada. Inicializando torneo...');

      const tournament = await tournamentService.getTournament(joinCode);
      console.log('📌 Estado inicial del torneo:', tournament);

      if (!tournament) {
        throw Error('Get Tournament failed');
      }

      updateTournamentUI(tournament);
      const leaveBtn = document.getElementById('leaveTournamentButton');
      const startBtn = document.getElementById('start-tournament-btn');

      if (tournament.status === 'in_progress') {
        leaveBtn?.classList.add('hidden');
        startBtn?.classList.add('hidden');
      }

      const profile = await profileService.getProfile();
      console.log('🧑 Perfil obtenido al cargar la página:', profile);

      if (profile) {
        console.log(
          '🔄 Actualizando torneo con el usuario que acaba de entrar...'
        );
        await tournamentService.updateTournamentWhenJoining(
          joinCode,
          tournament,
          profile.username
        );
      }
    } catch (error) {
      console.error('🔥 Error al inicializar el torneo:', error);
      showErrorToast(`Error initializing the game: ${error}`);
    }
  }

  // Setup interval for tournament status check
  intervalId = setInterval(async () => {
    console.log('⏳ Verificando estado del torneo...');

    const tournament = await tournamentService.getTournament(joinCode);
    console.log('📊 Estado del torneo actualizado:', tournament);

    updateTournamentUI(tournament);
    const leaveBtn = document.getElementById('leaveTournamentButton');
    const startBtn = document.getElementById('start-tournament-btn');

    if (tournament.status === 'in_progress') {
      leaveBtn?.classList.add('hidden');
      startBtn?.classList.add('hidden');
    }

    if (tournament.status === 'ready') {
      console.log(
        "✅ Torneo está en estado 'ready'. Verificando permisos para habilitar el botón..."
      );

      const profile = await profileService.getProfile();
      console.log('🧑 Perfil del usuario obtenido:', profile);

      if (!profile) {
        console.warn('⚠️ No se pudo obtener el perfil del usuario.');
        return;
      }

      const playerId = Number(profile.data.id);
      const leaderId = Number(tournament.players[0].id);

      if (playerId === leaderId) {
        console.log(
          '🎉 El usuario es el líder. Habilitando botón de inicio...'
        );
        document
          .getElementById('start-tournament-btn')
          .removeAttribute('disabled');
      } else {
        console.log('🔒 El usuario NO es el líder. Botón sigue deshabilitado.');
      }
    } else if (tournament.status === 'in_progress') {
      console.log(
        '🕹️ Torneo en progreso. Verificando si la ronda actual ha terminado...'
      );

      const roundMap = {
        1: 'quarter_finals',
        2: 'semi_finals',
        3: 'finals',
      };

      const currentRoundKey = roundMap[tournament.current_round];
      console.log(
        '📍 Ronda actual:',
        tournament.current_round,
        '->',
        currentRoundKey
      );

      const currentRoundFinished =
        tournament.matches.round_finished?.[currentRoundKey];

      if (currentRoundFinished) {
        console.log(
          `📢 La ronda '${currentRoundKey}' ha finalizado. Enviando señal para avanzar a la siguiente ronda...`
        );

        const result = await tournamentService.goToNextRound(tournament.id);

        if (!result) {
          console.error('❌ Error al avanzar a la siguiente ronda.');
          return;
        }

        console.log('✅ Siguiente ronda iniciada con éxito:', result);

        const nextRoundKey = {
          1: 'semi_finals',
          2: 'finals',
        }[tournament.current_round];

        if (nextRoundKey) {
          const profile = await profileService.getProfile();
          const currentUserId = profile?.data?.id;

          const newMatch = result.matches[nextRoundKey]?.find(
            match =>
              match?.player1?.id === currentUserId ||
              match?.player2?.id === currentUserId
          );

          if (newMatch?.match_id) {
            console.log(
              `🎮 Match encontrado para la nueva ronda (${nextRoundKey}):`,
              newMatch
            );
            await loadPage(
              `/game/${newMatch.match_id}/tournament/${result.join_code}`
            );
          } else {
            console.log(
              `🧘 El usuario no juega en esta ronda (${nextRoundKey}). Esperando a que termine...`
            );
          }
        }

        return;
      }

      console.log('🔍 Verificando partidos finalizados del usuario...');
      const matches = tournament.matches[currentRoundKey];
      const match = matches.find(match => match.game_finished);

      if (match) {
        console.log('✅ Se encontró un partido ya finalizado.');
        return;
      }

      clearInterval(intervalId);
      console.log('🛑 Intervalo de actualización detenido.');

      const profile = await profileService.getProfile();
      console.log('🧑 Perfil del usuario obtenido:', profile);

      if (!profile) {
        console.error('❌ No se pudo obtener el perfil del usuario.');
        return;
      }

      const currentUserId = profile.data.id;
      console.log('🔎 Buscando el match del usuario con ID:', currentUserId);

      const userMatchId = getUserMatch(tournament, currentUserId);
      if (!userMatchId) {
        console.error('❌ No se encontró un match para el usuario.');
        showErrorToast('No match found for your user.');
        return;
      }

      console.log('🎮 Redirigiendo al juego con match ID:', userMatchId);
      await loadPage(`/game/${userMatchId}/tournament/${tournament.join_code}`);
    }
  }, 1000);

  startTournamentBtn?.addEventListener('click', handleStartTournament);
  leaveTournamentButton?.addEventListener('click', handleLeaveTournament);
  window.addEventListener('popstate', handlePopState);
  window.addEventListener('beforeunload', handleBeforeUnload);
  window.addEventListener('storage', handleStorageChange);

  initializeTournament();

  return () => {
    clearInterval(intervalId);
    startTournamentBtn?.removeEventListener('click', handleStartTournament);
    leaveTournamentButton?.removeEventListener('click', handleLeaveTournament);
    window.removeEventListener('popstate', handlePopState);
    window.removeEventListener('beforeunload', handleBeforeUnload);
    window.removeEventListener('storage', handleStorageChange);
    leaveTournament();
  };
}
