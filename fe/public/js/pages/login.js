import { authService } from '../services/auth.js';
import { loadPage } from '../router/router.js';
import { CLIENT_ID, REDIRECT_URI } from '../utils/constants.js';

export function init() {
  const form = document.getElementById('loginForm');
  const togglePassword = document.getElementById('togglePassword');
  const login42Button = document.getElementById('login42Button');

  async function handleFormSubmit() {
    const user = {
      username: document.getElementById('username').value,
      password: document.getElementById('password').value,
    };

    const result = await authService.login(user);
    if (result) {
      await loadPage('/');
    }
  }

  function handleTogglePassword() {
    const passwordInput = document.getElementById('password');
    passwordInput.type =
      passwordInput.type === 'password' ? 'text' : 'password';
  }

  function handle42Login() {
    window.location.href = `https://api.intra.42.fr/oauth/authorize?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code`;
  }

  form?.addEventListener('formValid', handleFormSubmit);
  togglePassword?.addEventListener('click', handleTogglePassword);
  login42Button?.addEventListener('click', handle42Login);

  // Handle logout if needed
  if (window.location.pathname === '/logout') {
    handleLogout();
  }

  // Return cleanup function
  return () => {
    form?.removeEventListener('formValid', handleFormSubmit);
    togglePassword?.removeEventListener('click', handleTogglePassword);
    login42Button?.removeEventListener('click', handle42Login);
  };
}

// TODO: change this lol
async function handleLogout() {
  try {
    const response = await fetch('http://localhost:8000/api/auth/logout', {
      method: 'POST',
      credentials: 'include',
    });
    const data = await response.json();
    console.log('Logout successful:', data);
    window.location.href = '/';
  } catch (error) {
    console.error('Logout error:', error);
  }
}
