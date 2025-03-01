import { authService } from '../services/auth.js';
import { showErrorToast } from '../utils/helpers.js';
const form = document.getElementById('registerForm');

form.addEventListener('formValid', async () => {
  const user = {
    email: document.getElementById('email').value,
    username: document.getElementById('username').value,
    password: document.getElementById('password').value,
    password_confirmation: document.getElementById('password-confirmation')
      .value,
  };

  if (user.password !== user.password_confirmation) {
    showErrorToast('Passwords do not match');
    return;
  }

  await authService.register(user);
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
