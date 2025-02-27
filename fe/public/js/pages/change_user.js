import { API_URL } from '../utils/constants.js';
import { showErrorToast, showSuccessToast } from '../utils/helpers.js';

export const changeUser = {
  login: async (login, password) => {
    const response = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ login, password }),
    });

    const result = await response.json();

    if (!response.ok || !result?.success) {
      showErrorToast(result?.message || result?.error);
      return null;
    }

    showSuccessToast(result.message);
    return result.data || result;
  },
  register: async user => {
    const response = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(user),
    });

    const result = await response.json();

    if (!response.ok || !result?.success) {
      showErrorToast(result?.message || result?.error);
      return null;
    }

    showSuccessToast(result.message);
    return result.data || result;
  },
};