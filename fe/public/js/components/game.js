import { parseAndSetContent } from '../utils/helpers.js';

const appContainer = document.getElementById('app-container');

export async function loadGame(page) {
  try {
    console.log(`🎮 [loadGame] Intentando cargar el juego desde: ${page}`);

    const response = await fetch(page);
    if (!response.ok) {
      throw new Error('Error loading template or page content');
    }

    const responseContent = await response.text();
    appContainer.innerHTML = responseContent;
    console.log(`✅ [loadGame] Contenido insertado en appContainer.`);

    // Cargar scripts manualmente
    console.log("📌 [loadGame] Cargando game.js manualmente...");
    const script = document.createElement("script");
    script.src = "../../js/game.js";
    script.type = "module";
    script.defer = true;

    document.body.appendChild(script);
    console.log("✅ [loadGame] game.js cargado correctamente.");
  } catch (error) {
    console.error('Error loading game:', error.message);
  }
}


