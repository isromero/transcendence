import { API_URL } from '../utils/constants.js';

// TODO(ismael): Refactor this
export async function getUsers() {
  try {
    const response = await fetch(`${API_URL}/users`);
    if (!response.ok) {
      throw new Error('Failed to fetch users');
    }
    return await response.json();
  } catch (e) {
    console.error('Error fetching users:', e);
  }
}

export async function getUser(id) {
  try {
    const response = await fetch(`${API_URL}/users/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch user');
    }
    return await response.json();
  } catch (e) {
    console.error('Error fetching user:', e);
  }
}

export async function createUser(user) {
  try {
    const response = await fetch(`${API_URL}/users`, {
      method: 'POST',
      body: JSON.stringify(user),
    });
    if (!response.ok) {
      throw new Error('Failed to create user');
    }
    return await response.json();
  } catch (e) {
    console.error('Error creating user:', e);
  }
}

export async function updateUser(id, user) {
  try {
    const response = await fetch(`${API_URL}/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(user),
    });
    if (!response.ok) {
      throw new Error('Failed to update user');
    }
    return await response.json();
  } catch (e) {
    console.error('Error updating user:', e);
  }
}

export async function deleteUser(id) {
  try {
    const response = await fetch(`${API_URL}/users/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete user');
    }
    return await response.json();
  } catch (e) {
    console.error('Error deleting user:', e);
  }
}
