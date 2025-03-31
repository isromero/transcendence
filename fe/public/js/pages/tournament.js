import { profileService } from '../services/profile.js';
import { tournamentService } from '../services/tournaments.js';
import { showErrorToast, updateTournamentUI } from '../utils/helpers.js';
import { loadPage } from '../router/router.js';
import { initGame } from '../game.js';

function getJoinCodeFromURL() {
  const urlParts = window.location.pathname.split('/');
  const joinCode = urlParts[urlParts.length - 1];
  console.log("🔍 Código del torneo extraído de la URL:", joinCode);
  return joinCode;
}

const joinCode = getJoinCodeFromURL();
const startTournamentBtn = document.getElementById('start-tournament-btn');

if (!startTournamentBtn) {
  console.error("❌ Error: No se encontró el botón de inicio en el DOM.");
}

function getUserMatch(tournament, currentUserId) {
  console.log("🔎 Buscando el match del usuario en el torneo...", { tournament, currentUserId });

  const match = Object.values(tournament.matches)
    .flat()
    .find(
      match =>
        match?.player1?.id === currentUserId ||
        match?.player2?.id === currentUserId
    );

  console.log("🎯 Match encontrado para el usuario:", match);
  return match?.match_id;
}

startTournamentBtn?.addEventListener('click', async function () {
  try {
    console.log("🚀 Intentando iniciar el torneo...");
    
    const tournament = await tournamentService.getTournament(joinCode);
    console.log("📌 Datos del torneo al intentar iniciar:", tournament);
    
    if (!tournament) {
      console.error("❌ No se pudo obtener el torneo.");
      return;
    }

    if (tournament.current_players < tournament.max_players) {
      console.warn(`⚠️ No hay suficientes jugadores: ${tournament.current_players}/${tournament.max_players}`);
      showErrorToast(
        `Cannot start tournament. Waiting for more players. Current: ${tournament.current_players}/${tournament.max_players}`
      );
      return;
    }

    console.log("✅ Suficientes jugadores, iniciando torneo...");
    const tournamentId = tournament.id;
    const tournamentAfterStarting = await tournamentService.updateTournamentWhenStarting(tournamentId);

    console.log("🏁 Torneo después de iniciar:", tournamentAfterStarting);

    if (!tournamentAfterStarting) {
      console.error("❌ Error al actualizar el torneo después de iniciar.");
      return;
    }
  } catch (error) {
    console.error("🔥 Error inesperado al iniciar el torneo:", error);
    showErrorToast(
      `An error occurred while starting the tournament. ${error.message}`
    );
  }
});

const intervalId = setInterval(async () => {
  console.log("⏳ Verificando estado del torneo...");
  
  const tournament = await tournamentService.getTournament(joinCode);
  console.log("📊 Estado del torneo actualizado:", tournament);

  updateTournamentUI(tournament);

  if (tournament.status === 'ready') {
    console.log("✅ Torneo está en estado 'ready'. Verificando permisos para habilitar el botón...");
    
    const profile = await profileService.getProfile();
    console.log("🧑 Perfil del usuario obtenido:", profile);
    
    if (!profile) {
      console.warn("⚠️ No se pudo obtener el perfil del usuario.");
      return;
    }
    console.log("👀 Verificando liderazgo...");
    console.log("👤 ID del primer jugador en el torneo:", tournament.players[0]?.id);
    console.log("🧑 ID del usuario actual (desde profile):", profile);
    console.log("🆔 ID extraído de profile.data:", profile?.data?.id);
    

    const playerId = Number(profile.data.id); // Convertir ID del usuario a número
const leaderId = Number(tournament.players[0].id); // Convertir ID del líder a número

if (playerId === leaderId) {
    console.log("🎉 El usuario es el líder. Habilitando botón de inicio...");
    document.getElementById("start-tournament-btn").removeAttribute("disabled");
} else {
    console.log("🔒 El usuario NO es el líder. Botón sigue deshabilitado.");
}
  } else if (tournament.status === 'in_progress') {
    console.log("🕹️ Torneo en progreso. Buscando partido del usuario...");
    
    const roundMap = {
      1: 'quarter_finals',
      2: 'semi_finals',
      3: 'finals',
    };

    const currentRoundKey = roundMap[tournament.current_round];
    console.log("📍 Ronda actual:", tournament.current_round, "->", currentRoundKey);

    const matches = tournament.matches[currentRoundKey];
    const match = matches.find(match => match.game_finished);
    
    if (match) {
      console.log("✅ Se encontró un partido ya finalizado.");
      return;
    }

    clearInterval(intervalId);
    console.log("🛑 Intervalo de actualización detenido.");

    const profile = await profileService.getProfile();
    console.log("🧑 Perfil del usuario obtenido:", profile);

    if (!profile) {
      console.error("❌ No se pudo obtener el perfil del usuario.");
      return;
    }

    const currentUserId = profile.data.id;
    console.log("🔎 Buscando el match del usuario con ID:", currentUserId);

    const userMatchId = getUserMatch(tournament, currentUserId);
    if (!userMatchId) {
      console.error("❌ No se encontró un match para el usuario.");
      showErrorToast('No match found for your user.');
      return;
    }

    console.log("🎮 Redirigiendo al juego con match ID:", userMatchId);
    await loadPage(`/game/${userMatchId}/tournament/${tournament.join_code}`);
    await initGame();
  }
}, 1000);

async function leaveTournament() {
  console.log("🚪 Saliendo del torneo...");
  clearInterval(intervalId);

  const tournament = await tournamentService.getTournament(joinCode);
  console.log("📌 Datos del torneo al salir:", tournament);

  if (!tournament) {
    console.error("❌ Error: No se pudo obtener el torneo al intentar salir.");
    throw Error('Get Tournament failed');
  }

  await tournamentService.leaveTournament(joinCode, tournament);
  console.log("👋 Salida del torneo completada.");
}

window.addEventListener('popstate', async () => {
  console.log("🔄 Popstate event triggered.");
  
  const profile = await profileService.getProfile();
  if (!profile) return;

  const tournament = await tournamentService.getTournament(joinCode);
  console.log("📌 Estado del torneo al navegar:", tournament);

  if (!tournament || !tournament.players.some(p => p.id === profile.id)) {
    console.log("🏠 Redirigiendo al home porque el usuario no está en el torneo.");
    loadPage('/');
    return;
  }

  await leaveTournament();
});

window.addEventListener('beforeunload', async () => {
  console.log("⚠️ Evento beforeunload detectado. Saliendo del torneo...");
  await leaveTournament();
});

const leaveTournamentButton = document.getElementById('leaveTournamentButton');
leaveTournamentButton.addEventListener('click', async () => {
  console.log("🛑 Botón de salir presionado. Saliendo del torneo...");
  await leaveTournament();
  loadPage('/join-tournament');
});

if (
  document.readyState !== 'loading' &&
  window.location.pathname.includes('/tournament/')
) {
  try {
    console.log("📥 Página cargada. Inicializando torneo...");
    
    const tournament = await tournamentService.getTournament(joinCode);
    console.log("📌 Estado inicial del torneo:", tournament);

    if (!tournament) {
      throw Error('Get Tournament failed');
    }

    updateTournamentUI(tournament);

    const profile = await profileService.getProfile();
    console.log("🧑 Perfil obtenido al cargar la página:", profile);

    if (profile) {
      console.log("🔄 Actualizando torneo con el usuario que acaba de entrar...");
      console.log("📤 Datos enviados al servidor:", {
        joinCode,
        tournament,
        username: profile.data.username,
      });
      
      await tournamentService.updateTournamentWhenJoining(
        joinCode,
        tournament,
        profile.username
      );
    }
  } catch (error) {
    console.error("🔥 Error al inicializar el torneo:", error);
    showErrorToast(`Error initializing the game: ${error}`);
  }
}
