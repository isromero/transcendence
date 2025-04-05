import { authService } from '../services/auth.js';
import { showErrorToast } from '../utils/helpers.js';
import { loadPage } from '../router/router.js';

export function init() {
  const form = document.getElementById('registerForm');
  const togglePassword = document.getElementById('togglePassword');
  const togglePasswordConfirmation = document.getElementById(
    'togglePasswordConfirmation'
  );
  const privacyBanner = document.getElementById('privacy-banner');
  const acceptPrivacy = document.getElementById('accept-privacy');

  function updatePrivacyBannerVisibility() {
    if (privacyBanner) {
      privacyBanner.style.display = localStorage.getItem('privacyAccepted')
        ? 'none'
        : 'flex';
    }
  }

  async function handleFormSubmit() {
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
  }

  function handleTogglePassword() {
    const passwordInput = document.getElementById('password');
    passwordInput.type =
      passwordInput.type === 'password' ? 'text' : 'password';
  }

  function handleTogglePasswordConfirmation() {
    const passwordConfirmationInput = document.getElementById(
      'password-confirmation'
    );
    passwordConfirmationInput.type =
      passwordConfirmationInput.type === 'password' ? 'text' : 'password';
  }

  function handleAcceptPrivacy() {
    localStorage.setItem('privacyAccepted', 'true');
    updatePrivacyBannerVisibility();
  }

  updatePrivacyBannerVisibility();

  form?.addEventListener('formValid', handleFormSubmit);
  togglePassword?.addEventListener('click', handleTogglePassword);
  togglePasswordConfirmation?.addEventListener(
    'click',
    handleTogglePasswordConfirmation
  );
  acceptPrivacy?.addEventListener('click', handleAcceptPrivacy);

  return () => {
    form?.removeEventListener('formValid', handleFormSubmit);
    togglePassword?.removeEventListener('click', handleTogglePassword);
    togglePasswordConfirmation?.removeEventListener(
      'click',
      handleTogglePasswordConfirmation
    );
    acceptPrivacy?.removeEventListener('click', handleAcceptPrivacy);
  };
}
