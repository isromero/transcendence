import { API_URL } from '../utils/constants.js';
import { showErrorToast, showSuccessToast } from '../utils/helpers.js';
import { loadPage } from '../router/router.js';
import { usersService } from './users.js';

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

    if (!response.ok || !result?.success) {
      showErrorToast(result?.message || result?.error);
      return null;
    }

    await usersService.updateOnlineStatus(true);
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

    if (!response.ok || !result?.success) {
      showErrorToast(result?.message || result?.error);
      return null;
    }

    showSuccessToast(result.message);
    return result.data || result;
  },
  logout: async () => {
    // TODO: Implement in backend
    const response = await fetch(`${API_URL}/logout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      credentials: 'include',
    });

    const result = await response.json();

    if (!response.ok || !result?.success) {
      showErrorToast(result?.message || result?.error);
      return false;
    }

    await usersService.updateOnlineStatus(false);
    showSuccessToast(result.message);
    await loadPage('/auth');
    return true;
  },
};
