import { loadPage } from '../router/router.js';


document.addEventListener('click', async function (event) {
  if (event.target && event.target.id === 'local-match-btn') {
    event.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/history', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ local_match: true }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to create match.');
      }

      const matchId = data.data.match_id;
      console.log(`✅ Match ID recibido: ${matchId}`);

      // Verificar si el matchId es válido
      if (!matchId) {
        throw new Error('❌ Match ID no válido o vacío.');
      }

      window.history.pushState({}, '', `/game/${matchId}`);
      console.log(`✅ URL cambiada a /game/${matchId}`);

      // Llamar manualmente a la lógica de la SPA
      
      if (typeof loadPage === 'function') {
        console.log("📌 Antes de llamar loadPage...");

        console.log('🔄 Llamando a loadPage...');
        loadPage(`/game/${matchId}`);
        console.log("📌 Después de llamar loadPage...");

      } else {
        console.error('❌ loadPage no está definido.');
      }
    } catch (error) {
      console.error('❌ Error creando partida:', error);
      alert('Error creating match. Please try again.');
    }
  }
});
