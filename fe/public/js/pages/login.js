import { authService } from '../services/auth.js';
import { loadPage } from '../router/router.js';
const form = document.getElementById('loginForm');

form.addEventListener('formValid', async () => {
  const user = {
    username: document.getElementById('username').value,
    password: document.getElementById('password').value,
  };

  const result = await authService.login(user);
  if (result) {
    await loadPage('/');
  }
});

// Toggle password visibility
const togglePassword = document.getElementById('togglePassword');

togglePassword.addEventListener('click', () => {
  const passwordInput = document.getElementById('password');
  passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
});
