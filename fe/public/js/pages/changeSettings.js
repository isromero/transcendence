import { API_URL } from '../utils/constants.js';
import { showErrorToast, showSuccessToast } from '../utils/helpers.js';

export const changeSettings = {
  changeUser: async (login, password, id) => {
    const response = await fetch(`${API_URL}/login`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ login, password, id }),
    });

    const result = await response.json();

    if (!response.ok || !result?.success) {
      showErrorToast(result?.message || result?.error);
      return null;
    }

    showSuccessToast("username changed");
    return result.data || result;
  },
  changePassword: async (login, password, id) => {
    const response = await fetch(`${API_URL}/login`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ login, password, id }),
    });

    const result = await response.json();

    if (!response.ok || !result?.success) {
      showErrorToast(result?.message || result?.error);
      return null;
    }

    showSuccessToast("password changed");
    return result.data || result;
  },
};