// Manejo del historial y navegación
const appContainer = document.getElementById('app-container');

// Función para cargar dinámicamente una página en la SPA
async function loadPage(page) {
  try {
    const url = page === '/' ? '/index.html' : `/pages${page}.html`;
    const response = await fetch(url);

    // TODO (samu): Error pages
    if (!response.ok) throw new Error('Página no encontrada');

    const content = await response.text();
    appContainer.innerHTML = content;

    // Actualizar el historial del navegador
    window.history.pushState({ page }, '', page);
  } catch (error) {
    // TODO (samu): Error pages
    appContainer.innerHTML = '<div class="text-center"><h1>Error 404</h1><p>Página no encontrada.</p></div>';
  }
}

// Listener central para enlaces
document.body.addEventListener('click', (event) => {
  // Comprueba si el clic proviene de un enlace con la clase `spa-link`
  const link = event.target.closest('a.spa-link');
  if (link) {
    event.preventDefault(); // Evita la navegación estándar
    const page = link.getAttribute('href'); // Obtiene el destino del enlace
    loadPage(page); // Carga dinámicamente la página
  }
});

// Maneja la navegación hacia adelante y atrás en el historial del navegador
window.addEventListener('popstate', (event) => {
  const page = event.state?.page || '/';
  loadPage(page);
});

// Carga inicial
loadPage(window.location.pathname);