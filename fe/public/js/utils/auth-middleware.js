import { loadPage } from '../router/router.js';
import { API_URL } from '../utils/constants.js';

// List of public routes that don't require authentication in the frontend
const publicRoutes = [
  '/auth',
  '/auth/login',
  '/auth/register',
  '/auth/privacy',
  '/auth/help',
];

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
  const authenticated = await isAuthenticated();
  const isPublicRoute = publicRoutes.some(
    route => path === route || path.startsWith('/modal-')
  );

  // If authenticated and trying to access public routes (auth)
  // /auth/privacy is the only public route that should be accessible
  // for authenticated users
  if (authenticated && isPublicRoute && path !== '/auth/privacy') {
    await loadPage('/');
    return false;
  }

  // If not authenticated and trying to access protected routes
  if (!authenticated && !isPublicRoute) {
    await loadPage('/auth', { updateHistory: false });
    return false;
  }

  return true;
}
