import { API_URL } from '../utils/constants.js';
import { showErrorToast, showSuccessToast } from '../utils/helpers.js';

export const historyService = {
  createMatch: async () => {
    const response = await fetch(`${API_URL}/history`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ local_match: true }),
    });

    const result = await response.json();

    if (!response.ok || !result?.success) {
      showErrorToast(result?.message || result?.error);
      return null;
    }

    return result.data || result;
  },
  getMatch: async matchId => {
    const response = await fetch(`${API_URL}/history/${matchId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const result = await response.json();

    if (!response.ok || !result?.success) {
      showErrorToast(result?.message || result?.error);
      return null;
    }

    return result.data || result;
  },
};
