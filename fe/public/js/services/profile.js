import { API_URL } from '../utils/constants.js';
import { showErrorToast } from '../utils/helpers.js';

export const profileService = {
  getProfile: async () => {
    try {
      const response = await fetch(`${API_URL}/profile`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        credentials: 'include',
      });
      if (!response.ok) {
        throw new Error('Failed to fetch profile');
      }
      return await response.json();
    } catch (e) {
      showErrorToast(`Error fetching profile: ${e}`);
    }
  },
};
