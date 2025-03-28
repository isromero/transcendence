import { API_URL } from '../utils/constants.js';
import { showErrorToast, showSuccessToast } from '../utils/helpers.js';

export const tournamentService = {
  createTournament: async (tournamentName, maxPlayers) => {
    try {
      const response = await fetch(`${API_URL}/tournaments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({
          tournament_name: tournamentName,
          max_players: maxPlayers,
        }),
        credentials: 'include',
      });

      const result = await response.json();

      if (!response.ok || !result?.success) {
        if (result.error?.fields) {
          Object.entries(result.error.fields).forEach(([field, message]) => {
            showErrorToast(`${field}: ${message}`);
          });
        } else {
          showErrorToast("An unknown error occurred.");
        }
        return null;
      }

      showSuccessToast('Tournament created successfully!');
      return result.data || result;
    } catch (error) {
      showErrorToast(`Error creating tournament: ${error.message}`);
      return null;
    }
  },
  getTournament: async joinCode => {
    try {
      const response = await fetch(`${API_URL}/tournaments/${joinCode}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        credentials: 'include',
      });

      const result = await response.json();

      if (!response.ok || !result?.success) {
        if (result.error?.fields) {
          Object.entries(result.error.fields).forEach(([field, message]) => {
            showErrorToast(`${field}: ${message}`);
          });
        } else {
          showErrorToast("An unknown error occurred.");
        }
        return null;
      }

      return result.data || result;
    } catch (error) {
      showErrorToast(`Error fetching tournament data: ${error.message}`);
      return null;
    }
  },
  updateTournamentWhenJoining: async (
    joinCode,
    tournamentData,
    displayName
  ) => {
    try {
      const response = await fetch(`${API_URL}/tournaments`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({
          action: 'join',
          tournament_id: tournamentData.id,
          join_code: joinCode,
          displayName, // TODO: Currently not doing nothing in backend
        }),
        credentials: 'include',
      });

      const result = await response.json();

      if (!response.ok || !result?.success) {
        if (result.error?.fields) {
          Object.entries(result.error.fields).forEach(([field, message]) => {
            showErrorToast(`${field}: ${message}`);
          });
        } else {
          showErrorToast("An unknown error occurred.");
        }
        return null;
      }

      return result.data || result;
    } catch (error) {
      showErrorToast(`Error updating tournament: ${error.message}`);
      return null;
    }
  },
  updateTournamentWhenStarting: async tournamentId => {
    try {
      const response = await fetch(`${API_URL}/tournaments`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({
          action: 'start',
          tournament_id: tournamentId,
        }),
        credentials: 'include',
      });

      const result = await response.json();

      if (!response.ok || !result?.success) {
        if (result.error?.fields) {
          Object.entries(result.error.fields).forEach(([field, message]) => {
            showErrorToast(`${field}: ${message}`);
          });
        } else {
          showErrorToast("An unknown error occurred.");
        }
        return null;
      }

      showSuccessToast('Tournament started!');
      return result.data || result;
    } catch (error) {
      showErrorToast(`Error updating tournament: ${error.message}`);
      return null;
    }
  },
  leaveTournament: async (joinCode, tournamentData) => {
    try {
      const response = await fetch(`${API_URL}/tournaments`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({
          action: 'leave',
          tournament_id: tournamentData.id,
          join_code: joinCode,
        }),
        credentials: 'include',
      });

      const result = await response.json();

      if (!response.ok || !result?.success) {
        if (result.error?.fields) {
          Object.entries(result.error.fields).forEach(([field, message]) => {
            showErrorToast(`${field}: ${message}`);
          });
        } else {
          showErrorToast("An unknown error occurred.");
        }
        return null;
      }

      showSuccessToast('You leaved the tournament sucessfully');
      return result.data || result;
    } catch (error) {
      showErrorToast(`Error updating tournament: ${error.message}`);
      return null;
    }
  },
};
