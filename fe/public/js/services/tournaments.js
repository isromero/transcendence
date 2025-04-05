import { API_URL } from '../utils/constants.js';
import { showErrorToast, showSuccessToast } from '../utils/helpers.js';
import { profileService } from './profile.js';

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
        showErrorToast(result);
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
        showErrorToast(result);
        return null;
      }

      return result.data || result;
    } catch (error) {
      showErrorToast(`Error getting tournament: ${error.message}`);
      return null;
    }
  },

  updateTournamentWhenJoining: async (joinCode, tournament, displayName) => {
    try {
      const profile = await profileService.getProfile();
      if (!profile?.data?.id) {
        showErrorToast('Could not get user profile');
        return null;
      }

      const currentTournament = await tournamentService.getTournament(joinCode);
      if (!currentTournament) {
        showErrorToast('Tournament not found');
        return null;
      }

      const userId = profile.data.id;
      const tournamentKey = `tournament_${joinCode}_player_${userId}`;

      if (localStorage.getItem(tournamentKey)) {
        showErrorToast('You are already in this tournament');
        return null;
      }

      const response = await fetch(`${API_URL}/tournaments`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({
          action: 'join',
          tournament_id: currentTournament.id,
          join_code: joinCode,
          displayName,
        }),
        credentials: 'include',
      });

      const result = await response.json();

      if (!response.ok || !result?.success) {
        showErrorToast(result);
        return null;
      }

      localStorage.setItem(tournamentKey, 'true');
      showSuccessToast('You joined the tournament successfully!');
      return result.data || result;
    } catch (error) {
      showErrorToast(`Error joining tournament: ${error.message}`);
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
        showErrorToast(result);
        return null;
      }

      showSuccessToast('Tournament started!');
      return result.data || result;
    } catch (error) {
      showErrorToast(`Error updating tournament: ${error.message}`);
      return null;
    }
  },

  leaveTournament: async (joinCode, tournamentId) => {
    try {
      const profile = await profileService.getProfile();
      const userId = profile?.data?.id;
      const tournamentKey = `tournament_${joinCode}_player_${userId}`;

      const response = await fetch(`${API_URL}/tournaments`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({
          action: 'leave',
          tournament_id: tournamentId,
          join_code: joinCode,
        }),
        credentials: 'include',
      });

      const result = await response.json();

      if (!response.ok || !result?.success) {
        showErrorToast(result);
        return null;
      }

      localStorage.removeItem(tournamentKey);
      showSuccessToast('You left the tournament successfully');
      return result.data || result;
    } catch (error) {
      showErrorToast(`Error leaving tournament: ${error.message}`);
      return null;
    }
  },

  goToNextRound: async tournamentId => {
    try {
      const response = await fetch(`${API_URL}/tournaments`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({
          action: 'next_round',
          tournament_id: tournamentId,
        }),
        credentials: 'include',
      });

      const result = await response.json();

      if (!response.ok || !result?.success) {
        showErrorToast(result);
        return null;
      }

      showSuccessToast('Next round started successfully!');
      return result.data || result;
    } catch (error) {
      showErrorToast(`Error starting next round: ${error.message}`);
      return null;
    }
  },
};
