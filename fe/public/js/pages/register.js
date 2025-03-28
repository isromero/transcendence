import { authService } from '../services/auth.js';
import { showErrorToast } from '../utils/helpers.js';
import { loadPage } from '../router/router.js';
const form = document.getElementById('registerForm');

form.addEventListener('formValid', async () => {
  const user = {
    username: document.getElementById('username').value,
    password: document.getElementById('password').value,
    password_confirmation: document.getElementById('password-confirmation')
      .value,
  };

  if (user.password !== user.password_confirmation) {
    showErrorToast('Passwords do not match');
    return;
  }

  const result = await authService.register(user);
  if (result) {
    await loadPage('/auth');
  }
});

// Toggle password visibility
const togglePassword = document.getElementById('togglePassword');
const togglePasswordConfirmation = document.getElementById(
  'togglePasswordConfirmation'
);

togglePassword.addEventListener('click', () => {
  const passwordInput = document.getElementById('password');
  passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
});

togglePasswordConfirmation.addEventListener('click', () => {
  const passwordConfirmationInput = document.getElementById(
    'password-confirmation'
  );
  passwordConfirmationInput.type =
    passwordConfirmationInput.type === 'password' ? 'text' : 'password';
});
