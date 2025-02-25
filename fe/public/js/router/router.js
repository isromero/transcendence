import { pageMappings } from './routes.js';
import { loadModal, closeModal } from '../components/modal.js';
import { loadGame } from '../components/game.js';
import { loadMenu } from '../components/menu.js';
import { getCleanPageKey } from '../utils/helpers.js';
import { loadErrorPage } from '../components/error.js';

function matchRoute(path) {
  // Exact match
  if (pageMappings[path]) {
    return { url: pageMappings[path], params: {} };
  }

  // If not exact match, try dynamic routes
  for (const pattern in pageMappings) {
    const regexPattern = `${
      pattern
        .replace(/:[a-zA-Z]+/g, '([^/]+)') // :id -> ([^/]+)
        .replace(/\//g, '\\/') // Scape /
    }$`;

    const regex = new RegExp(regexPattern);
    const match = path.match(regex);

    if (match) {
      // Extract the names of the parameters from the original pattern
      const paramNames = pattern.match(/:[a-zA-Z]+/g) || [];
      const params = {};

      paramNames.forEach((name, index) => {
        params[name.substring(1)] = match[index + 1];
      });

      return { url: pageMappings[pattern], params };
    }
  }

  return null;
}

export async function loadPage(page) {
  try {
    closeModal();

    const cleanPage = getCleanPageKey(page).replace(/\/$/, '');
    const match = matchRoute(cleanPage);

    if (!match) {
      throw new Error(`Page ${cleanPage} not found`);
    }

    const { url, params } = match;

    if (url.includes('/components/')) {
      await loadModal(url, params);
    } else if (url.includes('/game/')) {
      await loadGame(url, params);
    } else {
      await loadMenu(url, params);
      window.history.pushState({ page: cleanPage, params }, '', cleanPage);
    }
  } catch (error) {
    console.error('Navigation error:', error);
    loadErrorPage(error.message);
  }
}
