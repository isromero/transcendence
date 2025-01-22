/* Punto de entrada */

// Selecciona el contenedor principal donde se cargará el contenido dinámico
const appContainer = document.getElementById('app-container');

// Función asincrónica para cargar el contenido de una página (por ejemplo, login.html)
async function loadPage(page) {
  try {
    // Realiza una solicitud HTTP para obtener el archivo HTML de la página
    const response = await fetch(`/pages/${page}.html`);
    
    // Verifica si la respuesta es correcta (200 OK). Si no, lanza un error.
    if (!response.ok) throw new Error('Página no encontrada');
    
    // Convierte la respuesta a texto (el contenido HTML de la página solicitada)
    const content = await response.text();
    
    // Reemplaza el contenido actual del contenedor principal con el contenido de la página
    appContainer.innerHTML = content; 
  } catch (error) {
    // Si ocurre un error (como que la página no existe), muestra un mensaje de error
    appContainer.innerHTML = '<h1>Error 404</h1><p>Página no encontrada.</p>';
  }
}

// Manejo de eventos para el clic en el botón "Login"
const btnLogin = document.getElementById('btn-login');

// Añade un "listener" de evento para detectar el clic en el botón "Login"
btnLogin.addEventListener('click', () => {
  // Cuando el botón "Login" es clickeado, se carga la página "login.html"
  loadPage('login');
});
