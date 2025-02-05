import { pageMappings } from './routes.js';
import { loadModal, closeModal } from '../components/modal.js';
import { loadGame } from '../components/game.js';
import { loadMenu } from '../components/menu.js';
import { getCleanPageKey } from '../utils/helpers.js';
import { loadErrorPage } from '../components/error.js';

export async function loadPage(page) {
  try {
    closeModal();

    const cleanPage = getCleanPageKey(page);
    const url = pageMappings[cleanPage];

    if (!url) {
      throw new Error(`Page ${cleanPage} not found`);
    }

    if (url.includes('/components/')) {
      await loadModal(url);
    } else if (url.includes('/game/')) {
      await loadGame(url);
    } else {
      await loadMenu(url);
      window.history.pushState({ page: cleanPage }, '', cleanPage);
    }
  } catch (error) {
    console.error('Navigation error:', error);
    loadErrorPage(error.message);
  }
}
