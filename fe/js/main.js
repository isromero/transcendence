// Manejo del historial y navegación
const appContainer = document.getElementById('app-container');

// Función para cargar una página dinámica en la SPA
async function loadPage(page) {
  try {
    // Determina la URL del archivo HTML a cargar según el nombre de la página
    const url = page === 'index' ? '/index.html' : `/pages/${page}.html`;
    const response = await fetch(url);

    // Verifica si la respuesta es válida; lanza un error si no lo es
    if (!response.ok) throw new Error('Página no encontrada');

    // Convierte la respuesta a texto (contenido HTML de la página)
    const content = await response.text();

    // Reemplaza el contenido actual del contenedor principal con el nuevo contenido
    appContainer.innerHTML = content;

    // Configura controladores de eventos para la página cargada
    setupPageHandlers(page);

    // Actualiza el historial del navegador para reflejar la nueva página
    window.history.pushState({ page }, '', page === 'index' ? '/' : `/${page}`);
  } catch (error) {
    // Si ocurre un error, muestra un mensaje de error genérico
    appContainer.innerHTML = '<div class="text-center"><h1>Error 404</h1><p>Página no encontrada.</p></div>';
  }
}

// Configura los controladores de eventos para cualquier página según el nombre de la página
function setupPageHandlers(page) {
  // Identifica y configura los controladores según la página cargada
  switch (page) {
    case 'index':
      setupIndexHandlers();
      break;
    case 'login':
      setupLoginHandlers();
      break;
    // Agrega más casos aquí según otras páginas
    default:
      console.warn(`No se han definido controladores para la página: ${page}`);
  }
}

// Configura los controladores de eventos específicos para la página "index"
function setupIndexHandlers() {
  const btnLogin = document.getElementById('btn-login');
  btnLogin?.addEventListener('click', () => {
    loadPage('login'); // Carga la página "login" cuando se hace clic
  });
}

// Configura los controladores de eventos específicos para la página "login"
function setupLoginHandlers() {
  // Botón "Cancelar" para volver al índice
  const cancelBtn = document.querySelector('.cancel-button');
  cancelBtn?.addEventListener('click', () => {
    loadPage('index'); // Carga la página de inicio ("index") cuando se hace clic
  });

  // Botón "Finish Login" para volver al índice después de iniciar sesión
  const finishLoginBtn = document.getElementById('finish-login');
  finishLoginBtn?.addEventListener('click', (event) => {
    event.preventDefault(); // Previene el comportamiento por defecto del formulario
    loadPage('index'); // Carga la página de inicio ("index")
  });
}

// Maneja la navegación hacia adelante y atrás en el historial del navegador
window.addEventListener('popstate', (event) => {
  const page = event.state?.page || 'index'; // Si no hay estado, usa "index" como valor por defecto
  loadPage(page);
});

// Configuración inicial al cargar la aplicación
loadPage('index'); // Carga la página inicial (index) al abrir la aplicación
