const appContainer = document.getElementById('app-container');

export async function loadGame(page) {
  try {
    const response = await fetch(page);
    if (!response.ok) {
      throw new Error('Error loading game');
    }
    appContainer.innerHTML = await response.text();
  } catch (error) {
    console.error('Game error:', error);
  }
}
