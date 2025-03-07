import { API_URL } from "../utils/constants.js";
import { showErrorToast, showSuccessToast } from '../utils/helpers.js';

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
  console.log("Button clicked!");  // Verifica si el evento de clic se dispara
  const joinCode = document.getElementById("join-code").textContent.split(":")[1].trim();  // Obtener el joinCode del HTML
  
  // Realizar la solicitud GET para obtener el ID del torneo usando el joinCode
  try {
      // Solicitar los detalles del torneo con el joinCode
      const getResponse = await fetch(`${API_URL}/tournaments/${joinCode}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
      });

      const tournamentData = await getResponse.json();
      console.log("Tournament data:", tournamentData);

      if (!getResponse.ok || !tournamentData?.id) {
          showErrorToast(tournamentData?.error || "Tournament not found or unavailable.");
          return; // Salir si no se encuentra el torneo
      }

      const tournamentId = tournamentData.id;  // Obtener el tournamentId del GET response
      
      // Enviar solicitud PUT para iniciar el torneo
      const response = await fetch(`${API_URL}/tournaments`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({
              action: "start",
              tournament_id: tournamentId,  // Usar el tournamentId extraído
          }),
      });

      console.log("EMPIEZA EL TORNEOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO");

      const result = await response.json();

      if (response.ok) {
          showSuccessToast("Tournament started successfully!");
      } else {
          showErrorToast(result?.error || "Failed to start the tournament.");
      }
  } catch (error) {
      console.error("Error starting tournament:", error);
      showErrorToast("An error occurred while starting the tournament.");
  }
});