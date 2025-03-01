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
    const matchedRoute = matchRoute(cleanPage);

    if (!matchedRoute) {
      throw new Error(`Page ${cleanPage} not found`);
    }

    // TODO: Params are not being used, is it needed for future use?
    // TODO: BTW, matchRoute is totally necessary because of dynamic routing
    // TODO: But the params returned are not being used
    const { url, params } = matchedRoute;

    if (url.includes('/components/')) {
      await loadModal(url);
    } else if (url.includes('/game/')) {
      await loadGame(url);
      window.history.replaceState({ page: cleanPage, params }, '', cleanPage);
    } else {
      await loadMenu(url);
      window.history.pushState({ page: cleanPage, params }, '', cleanPage);
    }
  } catch (error) {
    loadErrorPage(error.message);
  }
}
