import { pageMappings } from './routes.js';
import { loadModal, closeModal } from '../components/modal.js';
import { loadGame } from '../components/game.js';
import { loadMenu } from '../components/menu.js';
import { getCleanPageKey } from '../utils/helpers.js';
import { loadErrorPage } from '../components/error.js';
import { checkAuth } from '../utils/auth-middleware.js';

function matchRoute(path) {
  const normalizedPath = path === '' ? '/' : path;

  // Special case for root path
  if (normalizedPath === '/' && pageMappings[''] !== undefined) {
    return { url: pageMappings[''], params: {} };
  }

  // Exact match
  if (pageMappings[normalizedPath]) {
    return { url: pageMappings[normalizedPath], params: {} };
  }

  // If not exact match, try dynamic routes
  for (const pattern in pageMappings) {
    // Skip non-dynamic routes
    if (!pattern.includes(':')) {
      continue;
    }

    const regexPattern = `^${
      pattern
        .replace(/:[a-zA-Z]+/g, '([^/]+)') // :id -> ([^/]+)
        .replace(/\//g, '\\/') // Escape /
    }$`;

    const regex = new RegExp(regexPattern);
    const match = normalizedPath.match(regex);

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

    let cleanPage = getCleanPageKey(page).replace(/\/$/, '');

    // Check authentication before loading the page
    // Skip auth check for modals
    if (!cleanPage.startsWith('/modal-')) {
      const isAuthorized = await checkAuth(cleanPage);
      if (!isAuthorized) {
        return; // Auth middleware will handle the redirect
      }
    }

    const matchedRoute = matchRoute(cleanPage);

    if (cleanPage === '') {
      cleanPage = '/';
    }

    if (!matchedRoute) {
      throw new Error(`Page ${cleanPage} not found`);
    }

    // matchRoute es necesario para el enrutamiento dinámico, pero actualmente no usamos params.
    const { url } = matchedRoute; // Eliminamos `params` ya que no se usa.

    if (url.includes('/components/')) {
      await loadModal(url);
    } else if (url.includes('/game/')) {
      await loadGame(url);
      window.history.pushState({ page: cleanPage }, '', cleanPage); // Eliminamos `params` de `pushState`.
    } else {
      await loadMenu(url);
      window.history.pushState({ page: cleanPage }, '', cleanPage);
    }

    document.dispatchEvent(new CustomEvent('spaContentLoaded'));
  } catch (error) {
    loadErrorPage(error.message);
  }
}

