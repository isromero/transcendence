import { usersService } from '../services/users.js';
import { loadPage } from '../router/router.js';
import { profileService } from '../services/profile.js';
import { showErrorToast } from '../utils/helpers.js';
export function init() {
  const form = document.getElementById('accountDeletionForm');
  const passwordInput = document.getElementById('password');
  const togglePassword = document.getElementById('togglePassword');
  const passwordFieldWrapper = document.getElementById('passwordFieldWrapper');

  async function handleFormSubmit() {
    try {
      const profile = await profileService.getProfile();
      const username = String(profile?.data?.username ?? '');

      const isOAuthUser = username.length < 9;

      if (isOAuthUser) {
        const ok = await usersService.deleteUserWithoutPassword();
        if (ok) {
          loadPage('/auth', { updateHistory: false });
        }
      } else {
        const ok = await usersService.deleteUser(passwordInput.value);
        if (ok) {
          loadPage('/auth', { updateHistory: false });
        }
      }
    } catch (e) {
      console.error('Error handling form submission:', e);
      showErrorToast('An error occurred while processing your request.');
    }
  }

  function handleTogglePassword() {
    passwordInput.type =
      passwordInput.type === 'password' ? 'text' : 'password';
  }

  async function initForm() {
    try {
      const profile = await profileService.getProfile();
      const username = String(profile?.data?.username ?? '');

      if (username.length >= 9) {
        passwordFieldWrapper.style.display = 'block';
      } else {
        passwordFieldWrapper.style.display = 'none';
      }
    } catch (e) {
      console.error('Error loading profile:', e);
    }
  }

  form?.addEventListener('formValid', handleFormSubmit);
  togglePassword?.addEventListener('click', handleTogglePassword);

  initForm();

  return () => {
    form?.removeEventListener('formValid', handleFormSubmit);
    togglePassword?.removeEventListener('click', handleTogglePassword);
  };
}
