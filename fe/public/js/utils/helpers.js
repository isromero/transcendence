import { pageMappings } from '../router/routes.js';

export function getCleanPageKey(requestedPath) {
  if (pageMappings[requestedPath]) {
    return requestedPath;
  }
  return (
    Object.keys(pageMappings).find(
      key => pageMappings[key] === requestedPath
    ) || requestedPath
  );
}
