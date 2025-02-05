const appContainer = document.getElementById('app-container');

export async function loadMenu(page) {
  try {
    const templateResponse = await fetch('/pages/templates/menu.html');
    if (!templateResponse.ok) {
      throw new Error('Error loading menu template');
    }

    const templateContent = await templateResponse.text();
    appContainer.innerHTML = templateContent;

    const pageContainer = document.getElementById('page-container');
    const contentResponse = await fetch(page);
    if (!contentResponse.ok) {
      throw new Error('Error loading menu content');
    }

    const pageContent = await contentResponse.text();
    pageContainer.innerHTML = pageContent;
    updateIcons(page);
  } catch (error) {
    console.error('Menu error:', error);
  }
}

function updateIcons(page) {
  const leftButton = document.querySelector(
    '.btn.position-absolute.bottom-0.start-0 i'
  );
  const rightButton = document.querySelector(
    '.btn.position-absolute.bottom-0.end-0 i'
  );

  if (!leftButton || !rightButton) {
    console.warn('Navigation buttons not found in the DOM');
    return;
  }

  // Extract the page type from the URL
  const isMenuPage = page.includes('/pages/menus/');
  const isGamePage = page.includes('/pages/game/');
  const pageType = page.split('/').pop().replace('.html', '');

  // Set default attributes
  leftButton.className = 'bi bi-person-circle';
  leftButton.parentElement.setAttribute('href', '/profile');
  rightButton.className = 'bi bi-list';
  rightButton.parentElement.setAttribute('href', '/settings');

  // Special cases for authentication pages
  if (pageType === 'auth' || pageType === 'login' || pageType === 'register') {
    leftButton.className = 'bi bi-question-circle';
    leftButton.parentElement.setAttribute('href', '/modal-help');
    rightButton.className = 'bi bi-globe';
    rightButton.parentElement.setAttribute('href', '/modal-languages');
  }

  // Special cases for game pages
  if (isGamePage) {
    leftButton.className = 'bi bi-arrow-left';
    leftButton.parentElement.setAttribute('href', '/auth');
    rightButton.className = 'bi bi-pause';
    rightButton.parentElement.setAttribute('href', '/modal-pause');
  }
}
