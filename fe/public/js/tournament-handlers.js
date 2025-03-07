// tournament-handlers.js - Updated approach
import { loadPage } from './router/router.js';
import { API_URL } from './utils/constants.js';
import { showErrorToast } from './utils/helpers.js';

console.log("tournament-handlers.js loaded");

// Define the createTournament function directly in this file
async function createTournament(tournamentName, maxPlayers) {
  try {
    console.log(`Creating tournament: ${tournamentName} with ${maxPlayers} players`);
    
    const response = await fetch(`${API_URL}/tournaments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        tournament_name: tournamentName,
        max_players: maxPlayers,
      }),
      credentials: 'include',
    });
    
    console.log("Response received:", response);
    const result = await response.json();
    console.log("Result data:", result);
    
    if (!response.ok || !result?.success) {
      showErrorToast(result?.message || result?.error || "Failed to create tournament");
      return null;
    }
    
    console.log("Tournament created successfully:", result);
    return result.data || result;
  } catch (error) {
    console.error("Error creating tournament:", error);
    showErrorToast("Error creating tournament: " + error.message);
    return null;
  }
}

// Add a global click event listener similar to your multiplayer approach
document.addEventListener('click', async function(event) {
  if (event.target && event.target.id === '4-players-btn') {
    event.preventDefault();
    console.log("4 players button clicked via global listener");
    const tournamentNameInput = document.getElementById("tournament-name");
    const tournamentName = tournamentNameInput.value.trim() || "Tournament 4 Players";
    
    const result = await createTournament(tournamentName, 4);
    if (result) {
      console.log("Tournament created, navigating to:", result);
      loadPage(`/tournament/${result.join_code}`);    }
  }
  
  if (event.target && event.target.id === '8-players-btn') {
    event.preventDefault();
    console.log("8 players button clicked via global listener");
    const tournamentNameInput = document.getElementById("tournament-name");
    const tournamentName = tournamentNameInput.value.trim() || "Tournament 8 Players";
    
    const result = await createTournament(tournamentName, 8);
    if (result) {
      console.log("Tournament created, navigating to:", result);
      loadPage(`/tournament/${result.join_code}`);    }
  }
});

