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
    loadPage('/');
  }
});

// Toggle password visibility
const togglePassword = document.getElementById('togglePassword');

togglePassword.addEventListener('click', () => {
  const passwordInput = document.getElementById('password');
  passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
});

const login42Button = document.querySelector('[data-translationKey="login42"]');
if (login42Button) {
  login42Button.addEventListener("click", function () {
    window.location.href = `http://${window.location.hostname}:8000/api/auth/login`;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  if (window.location.pathname === "/logout") {
      fetch(`http://${window.location.hostname}:8000/api/auth/logout`, {
          method: "POST",
          credentials: "include",
      })
      .then(response => response.json())
      .then(data => {
          console.log("Logout successful:", data);
          window.location.href = "/"; // Redirige a la home tras cerrar sesión
      })
      .catch(error => console.error("Logout error:", error));
  }
});
