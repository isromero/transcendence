import { API_URL } from '../utils/constants.js';
import { showErrorToast, showSuccessToast } from '../utils/helpers.js';

export const friendsService = {
  getFriends: async () => {
    try {
      const response = await fetch(`${API_URL}/friends`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        credentials: 'include',
      });
      if (!response.ok) {
        throw new Error('Failed to fetch friends');
      }
      const result = await response.json();
      return result.data;
    } catch (e) {
      console.error('Error fetching friends:', e);
    }
  },
  getRequests: async () => {
    try {
      const response = await fetch(`${API_URL}/friends?action=requests`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        credentials: 'include',
      });
      if (!response.ok) {
        throw new Error('Failed to fetch friend requests');
      }
      const result = await response.json();
      return result.data;
    } catch (e) {
      console.error('Error fetching friend requests:', e);
    }
  },
  addFriend: async friend => {
    try {
      const response = await fetch(`${API_URL}/friends`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify(friend),
        credentials: 'include',
      });

      const result = await response.json();

      if (!response.ok || !result?.success) {
        showErrorToast(result);
        return null;
      }

      showSuccessToast(result.message);
      return result.data || result;
    } catch (e) {
      showErrorToast(`Error creating friend: ${e}`);
    }
  },
  respondToRequest: async (userId, action) => {
    try {
      const response = await fetch(`${API_URL}/friends/${userId}/${action}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        credentials: 'include',
      });

      const result = await response.json();

      if (!response.ok || !result?.success || result.error) {
        showErrorToast(result);
        return null;
      }

      showSuccessToast(result.message);
      return result.data || result;
    } catch (e) {
      showErrorToast(`Error responding to friend request: ${e}`);
    }
  },
  deleteUser: async () => {
    try {
      const response = await fetch(`${API_URL}/friends`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        credentials: 'include',
      });

      if (response.status === 204) {
        showSuccessToast('Friend succesfully deleted');
        return true;
      }

      if (!response.ok) {
        showErrorToast('Error deleting friend');
        return false;
      }

      return false;
    } catch (e) {
      showErrorToast(`Error deleting friend: ${e}`);
      return false;
    }
  },
};
