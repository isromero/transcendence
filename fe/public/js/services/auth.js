import { API_URL } from '../utils/constants.js';
import { showErrorToast, showSuccessToast } from '../utils/helpers.js';
import { loadPage } from '../router/router.js';

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

    if (result.error)
    {
      console.log(result.error.fields.username); // "Username can only contain letters, numbers, underscores and hyphens"
      console.log(result.error.fields["__all__"]); // "Password must contain at least one number"
    }
    
    if (!response.ok || !result?.success || result.error) {
      if (result.error.fields.username)
        showErrorToast(`username: ${result?.error.fields.username}`);
      else
      {
        console.log(result.error);
        if (result.error.password === 'undefined')
        {
          showErrorToast(`password: tonto`);
        }
        showErrorToast(`password: ${result?.error.fields.password}`);
      }
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

    showSuccessToast(result.message);
    loadPage('/auth');
    return true;
  },
};
