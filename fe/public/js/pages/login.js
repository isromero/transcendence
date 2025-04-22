import { authService } from '../services/auth.js';
import { loadPage } from '../router/router.js';
import { API_AUTH_LOGIN_FOR_42 } from '../utils/constants.js';
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
      await loadPage('/', { updateHistory: false });
    }
  }

  function handleTogglePassword() {
    const passwordInput = document.getElementById('password');
    passwordInput.type =
      passwordInput.type === 'password' ? 'text' : 'password';
  }

  function handle42Login() {
    window.location.href = API_AUTH_LOGIN_FOR_42;
  }

  form?.addEventListener('formValid', handleFormSubmit);
  togglePassword?.addEventListener('click', handleTogglePassword);
  login42Button?.addEventListener('click', handle42Login);

  return () => {
    form?.removeEventListener('formValid', handleFormSubmit);
    togglePassword?.removeEventListener('click', handleTogglePassword);
    login42Button?.removeEventListener('click', handle42Login);
  };
}
