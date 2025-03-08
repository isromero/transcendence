import { API_URL } from "../utils/constants.js";
import { showErrorToast, showSuccessToast } from '../utils/helpers.js';
import { loadPage } from '../router/router.js';
import { initGame } from '../game.js';

// Obtener el join_code desde la URL
function getJoinCodeFromURL() {
  const urlParts = window.location.pathname.split("/");
  return urlParts[urlParts.length - 1]; // Última parte de la URL es el join_code
}

// Función para obtener los datos del torneo usando el join_code
async function fetchTournamentData(joinCode) {
  try {
    const response = await fetch(`${API_URL}/tournaments/${joinCode}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    });

    if (!response.ok) {
      throw new Error("Error fetching tournament data");
    }

    const tournamentData = await response.json();
    console.log("Tournament data:", tournamentData);
    updateTournamentUI(tournamentData);
  } catch (error) {
    console.error("Failed to fetch tournament data:", error);
  }
}

// Función para actualizar la UI con los datos del torneo
function updateTournamentUI(tournamentData) {
  // Actualizar nombre del torneo y código de unión
  document.getElementById("tournament-name").textContent = tournamentData.tournament_name;
  document.getElementById("join-code").textContent = `Join Code: ${tournamentData.join_code}`;

  // Rellenar los jugadores en los huecos disponibles
  const playerSlots = document.querySelectorAll(".player-info span");
  tournamentData.players.forEach((player, index) => {
    if (playerSlots[index]) {
      playerSlots[index].textContent = player.username;
      playerSlots[index].previousElementSibling.src = player.avatar || "../assets/images/default-avatar.jpg";
    }
  });
}

// Iniciar la actualización automática
const joinCode = getJoinCodeFromURL();

// Almacenar el ID del intervalo para poder limpiarlo después
const intervalId = setInterval(() => fetchTournamentData(joinCode), 10000); // Actualiza cada 10 segundos

// Llamar a fetchTournamentData inicialmente para la primera carga
fetchTournamentData(joinCode);

// Limpiar el intervalo cuando la ventana o página sea cerrada
window.addEventListener("beforeunload", () => {
  clearInterval(intervalId); // Detener el intervalo
});


document.getElementById("start-tournament-btn")?.addEventListener("click", async function () {
  console.log("Button clicked!");  
  const joinCode = document.getElementById("join-code").textContent.split(":")[1].trim();  

  try {
      // 1️⃣ Obtener el usuario actual desde /profile
      const userResponse = await fetch(`${API_URL}/profile`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
      });

      const userData = await userResponse.json();
      console.log("Raw userData:", userData);  // 👀 Ver qué devuelve la API

      if (!userResponse.ok || !userData?.data?.id) {  // ⚠️ Cambiado
          showErrorToast("Failed to get user data.");
          return;
      }

      const currentUserId = userData.data.id;  // ⚠️ Cambiado
      console.log("Current user ID:", currentUserId);

      // 2️⃣ Obtener el torneo para extraer el tournamentId
      const getResponse = await fetch(`${API_URL}/tournaments/${joinCode}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
      });

      const tournamentData = await getResponse.json();
      if (!getResponse.ok || !tournamentData?.id) {
          showErrorToast("Tournament not found.");
          return;
      }

      const tournamentId = tournamentData.id;

      // 3️⃣ Iniciar el torneo y recibir los partidos con los match_id
      const response = await fetch(`${API_URL}/tournaments`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({ action: "start", tournament_id: tournamentId }),
      });

      const result = await response.json();
      if (!response.ok || !result?.matches) {
          showErrorToast(result?.error || "Failed to start tournament.");
          return;
      }

      console.log("Tournament started:", result);

      showSuccessToast("Tournament started!");

      // 4️⃣ Buscar el partido del usuario
      let userMatchId = null;
      Object.values(result.matches).flat().forEach(match => {
          if (match.player1?.id === currentUserId || match.player2?.id === currentUserId) {
              userMatchId = match.match_id;
          }
      });
      
      if (!userMatchId) {
          showErrorToast("No match found for your user.");
          return;
      }

      console.log("User match ID:", userMatchId);

      // 5️⃣ Redirigir a la partida del usuario
      await loadPage(`/game/${userMatchId}`);
      await initGame();

  } catch (error) {
      console.error("Error starting tournament:", error);
      showErrorToast("An error occurred while starting the tournament.");
  }
});
