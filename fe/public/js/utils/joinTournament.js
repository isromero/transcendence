console.log("joinTournament.js loaded");


import { API_URL } from './constants.js';
import { showErrorToast, showSuccessToast } from './helpers.js';
import { loadPage } from '../router/router.js';



// Function to join a tournament
async function joinTournament(username, joinCode) {
  try {
    console.log(`Attempting to join tournament with code: ${joinCode}`);

    // Step 1: Get tournament details using joinCode
    const getResponse = await fetch(`${API_URL}/tournaments/${joinCode}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
    });

    const tournamentData = await getResponse.json();
    // console.log("Tournament data:", tournamentData);

    if (!getResponse.ok || !tournamentData?.id) {
      showErrorToast(tournamentData?.error || "Tournament not found or unavailable.");
      return null;
    }

    // Step 2: Send request to join the tournament
    const putResponse = await fetch(`${API_URL}/tournaments`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        action: "join",
        tournament_id: tournamentData.id,  // Pass tournament_id in the body
        join_code: joinCode,
        username: username,
      }),
    });

    const putResult = await putResponse.json();
    console.log("Join response:", putResult);

    if (!putResponse.ok || putResult?.error) {
      showErrorToast(putResult?.error || "Failed to join tournament.");
      return null;
    }

    showSuccessToast("Successfully joined the tournament!");

    // Redirect to the tournament page
    setTimeout(() => {
      loadPage(`/tournament/${joinCode}`);
    }, 2000);

    return tournamentData;
  } catch (error) {
    console.error("Error joining tournament:", error);
    showErrorToast("An error occurred while joining the tournament.");
    return null;
  }
}

// Add event listener for form submission
console.log("Join Tournament script loaded!");
document.getElementById("joinTournamentForm").addEventListener("submit", async function (event) {
  event.preventDefault();

  const username = document.getElementById("username").value.trim();
  const joinCode = document.getElementById("joinCode").value.trim();

  if (!username || !joinCode) {
    showErrorToast("Please fill in all fields.");
    return;
  }

  const tournamentData = await joinTournament(username, joinCode);
  if (tournamentData) {
    // Tournament joined successfully, proceed to the next steps if needed
    // console.log("Tournament data after joining:", tournamentData);
  }
});



  
