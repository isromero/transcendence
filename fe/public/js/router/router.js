import { pageMappings } from './routes.js';
import { loadModal, closeModal } from '../components/modal.js';
import { loadGame } from '../components/game.js';
import { loadMenu } from '../components/menu.js';
import { getCleanPageKey } from '../utils/helpers.js';
import { loadErrorPage } from '../components/error.js';
import { checkAuth } from '../utils/auth-middleware.js';
import { pageControllers } from '../utils/pageControllers.js';

function matchRoute(path) {
  const normalizedPath = path === '' ? '/' : path;

  // Special case for root path
  if (normalizedPath === '/' && pageMappings[''] !== undefined) {
    return {
      pattern: '/',
      url: pageMappings[''],
      params: {},
    };
  }

  // Exact match
  if (pageMappings[normalizedPath]) {
    return {
      pattern: normalizedPath,
      url: pageMappings[normalizedPath],
      params: {},
    };
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

      return {
        pattern,
        url: pageMappings[pattern],
        params,
      };
    }
  }

  return null;
}

let currentCleanup = null;

export async function loadPage(page, { updateHistory = true } = {}) {
  try {
    if (currentCleanup) {
      currentCleanup();
      currentCleanup = null;
    }

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

    const { url, params } = matchedRoute;

    if (url.includes('/components/')) {
      await loadModal(url);
    } else if (url.includes('/game/')) {
      await loadGame(url);
      if (updateHistory) {
        window.history.pushState({ page: cleanPage }, '', cleanPage);
      }
    } else {
      await loadMenu(url);
      if (updateHistory) {
        window.history.pushState({ page: cleanPage }, '', cleanPage);
      }
    }

    const controller = pageControllers[matchedRoute.pattern];
    if (controller?.init) {
      currentCleanup = await controller.init(params);
    }
  } catch (error) {
    loadErrorPage(error.message);
  }
}
