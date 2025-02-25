// TODO(adri): This is a temporal file, maybe we need to structure the code better or refactor
document.addEventListener('DOMContentLoaded', () => {
  document
    .getElementById('local-match-btn')
    .addEventListener('click', async function (event) {
      event.preventDefault();
      try {
        const response = await fetch('http://localhost:8000/api/history', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            local_match: true,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || 'Failed to create match.');
        }

        const matchId = data.data.match_id;

        // Buscar el enlace <a>
        const gameLink = document.getElementById('gameLink');

        if (gameLink) {
          // Si el enlace existe, cambiar href y simular clic
          gameLink.href = `/game/${matchId}`;
          gameLink.click();
        } else {
          // Si no existe, cambiar la URL manualmente con pushState
          window.history.pushState({}, '', `/game/${matchId}`);
          console.log(`URL changed to /game/${matchId}`);

          // Llamar manualmente a la lógica de la SPA si es necesario
          /*  if (typeof onRouteChange === 'function') {
            onRouteChange(`/game/${matchId}`);
          } */
        }
      } catch (error) {
        console.error('Error creating match:', error);
        alert('Error creating match. Please try again.');
      }
    });
});
