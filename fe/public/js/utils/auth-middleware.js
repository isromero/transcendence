import { loadPage } from '../router/router.js';
import { API_URL } from '../utils/constants.js';

// List of public routes that don't require authentication in the frontend
const publicRoutes = ['/auth', '/auth/login', '/auth/register'];

// Check if the user is authenticated by making a request to the backend
export async function isAuthenticated() {
  try {
    const response = await fetch(`${API_URL}/check-auth`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      credentials: 'include',
    });

    return response.ok;
  } catch (error) {
    console.error('Auth check failed:', error);
    return false;
  }
}

// Middleware function to check authentication before loading a page
export async function checkAuth(path) {
  // If it's a public route, allow access
  if (
    publicRoutes.some(route => path === route || path.startsWith('/modal-'))
  ) {
    return true;
  }

  // If user is authenticated, allow access
  const authenticated = await isAuthenticated();
  if (authenticated) {
    return true;
  }

  // If not authenticated and trying to access protected route, redirect to auth
  loadPage('/auth');
  return false;
}
