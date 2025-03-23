import { API_URL } from '../utils/constants.js';
import { showErrorToast, showSuccessToast } from '../utils/helpers.js';

export const authService = {
  login: async user => {
    const response = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify(user),
      credentials: 'include',
    });

    const result = await response.json();

    if (!response.ok || !result?.success || result.error) {
      if (result.error?.fields) {
        Object.entries(result.error.fields).forEach(([field, message]) => {
          showErrorToast(`${field}: ${message}`);
        });
      } else {
        showErrorToast("An unknown error occurred.");
      }
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
        Accept: 'application/json',
      },
      body: JSON.stringify(user),
    });

    const result = await response.json();
   
    if (!response.ok || !result?.success || result.error) {
      if (result.error?.fields) {
        Object.entries(result.error.fields).forEach(([field, message]) => {
          showErrorToast(`${field}: ${message}`);
        });
      } else {
        showErrorToast("An unknown error occurred.");
      }
      return null;
    }
    showSuccessToast(result.message);
    return result.data || result;
  },
  logout: async () => {
    const response = await fetch(`${API_URL}/logout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      credentials: 'include',
    });

    const result = await response.json();

    if (!response.ok || !result?.success || result.error) {
      if (result.error?.fields) {
        Object.entries(result.error.fields).forEach(([field, message]) => {
          showErrorToast(`${field}: ${message}`);
        });
      } else {
        showErrorToast("An unknown error occurred.");
      }
    }

    showSuccessToast(result.message);
    return true;
  },
};
