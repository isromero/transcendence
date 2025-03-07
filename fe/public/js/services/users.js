import { API_URL } from '../utils/constants.js';
import { showErrorToast, showSuccessToast } from '../utils/helpers.js';

export const usersService = {
  getUsers: async () => {
    try {
      const response = await fetch(`${API_URL}/users`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        credentials: 'include',
      });
      if (!response.ok) {
        throw new Error('Failed to fetch users');
      }
      return await response.json();
    } catch (e) {
      console.error('Error fetching users:', e);
    }
  },
  getUser: async id => {
    try {
      const response = await fetch(`${API_URL}/users/${id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        credentials: 'include',
      });
      if (!response.ok) {
        throw new Error('Failed to fetch user');
      }
      return await response.json();
    } catch (e) {
      console.error('Error fetching user:', e);
    }
  },
  updateUser: async user => {
    try {
      const response = await fetch(`${API_URL}/users`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify(user),
        credentials: 'include',
      });

      const result = await response.json();

      if (!response.ok || !result?.success) {
        showErrorToast(result?.message);
        return null;
      }

      showSuccessToast(result.message);
      return result.data || result;
    } catch (e) {
      console.error('Error updating user:', e);
      showErrorToast('Network error');
    }
  },
  deleteUser: async id => {
    try {
      const response = await fetch(`${API_URL}/users/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        credentials: 'include',
      });

      const result = await response.json();

      if (!response.ok || !result?.success) {
        showErrorToast(result?.message);
        return null;
      }

      showSuccessToast(result.message);
      return result.data || result;
    } catch (e) {
      console.error('Error deleting user:', e);
      showErrorToast('Network error');
    }
  },
};
