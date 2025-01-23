const appContainer = document.getElementById('app-container');

// Función para cargar una página
async function loadPage(page) {
  try {
    const url = page === '/' ? '/index.html' : `/pages${page}.html`;
    const response = await fetch(url);

    if (!response.ok) throw new Error('Página no encontrada');

    const content = await response.text();
    appContainer.innerHTML = content;

    // Cambia el estado del historial
    window.history.pushState({ page }, '', page);

    // Actualiza los iconos después de cargar la nueva página
    updateIcons(page);
  } catch (error) {
    appContainer.innerHTML = '<div class="text-center"><h1>Error 404</h1><p>Página no encontrada.</p></div>';
  }
}

// Función para actualizar los iconos según la página
function updateIcons(page) {
  const leftButton = document.querySelector('.btn.position-absolute.bottom-0.start-0 i');
  const rightButton = document.querySelector('.btn.position-absolute.bottom-0.end-0 i');

  if (page === '/login') {
    // Cambiar iconos para la página "friends"
    leftButton.className = 'bi bi-question-circle'; // Cambia a un icono de perfil
    rightButton.className = 'bi bi-globe'; 
  } else if (page === '/register') {
    // Cambiar iconos para la página "register"
    leftButton.className = 'bi bi-question-circle'; // Cambia a un icono de perfil
    rightButton.className = 'bi bi-globe'; 
  }
  else if (page === '/') {
    // Cambiar iconos para la página "register"
    leftButton.className = 'bi bi-question-circle'; // Cambia a un icono de perfil
    rightButton.className = 'bi bi-globe'; 
  }
   else {
    // Iconos por defecto
    leftButton.className = 'bi bi-person-circle'; // Cambia a un icono de perfil
    leftButton.parentElement.setAttribute('href', '/profile'); // Establece el href a /profile
    rightButton.className = 'bi bi-list'; 
  }
}

// Event listener para enlaces SPA
document.body.addEventListener('click', (event) => {
  const link = event.target.closest('a.spa-link');
  if (link) {
    event.preventDefault();
    const page = link.getAttribute('href');
    loadPage(page);
  }
});

// Manejar el evento "popstate"
window.addEventListener('popstate', (event) => {
  const page = event.state?.page || '/';
  loadPage(page);
});

// Cargar la página inicial
loadPage(window.location.pathname);
