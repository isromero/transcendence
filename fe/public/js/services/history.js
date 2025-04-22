import { loadErrorPage } from '../components/error.js';
import { API_URL } from '../utils/constants.js';
import { showErrorToast } from '../utils/helpers.js';

export const historyService = {
  createMatch: async () => {
    const response = await fetch(`${API_URL}/history`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({ type_match: 'local' }),
      credentials: 'include',
    });

    const result = await response.json();

    if (!response.ok || !result?.success || result.error) {
      showErrorToast(result);
      return null;
    }
    return result.data || result;
  },
  getMatch: async matchId => {
    const response = await fetch(`${API_URL}/history/${matchId}`, {
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
  },
  getMatchHistory: async matchId => {
    const response = await fetch(`${API_URL}/history/match/${matchId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      showErrorToast('This match does not exist');
      loadErrorPage('Match not found');
      return null;
    }

    const result = await response.json();

    if (!response.ok || !result?.success) {
      showErrorToast(result);
      return null;
    }

    return result.data || result;
  },
};
