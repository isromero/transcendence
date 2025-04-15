import { changeLanguage } from '../pages/languages.js';
import { parseAndSetContent } from '../utils/helpers.js';
import { initGlobalValidation } from '../utils/helpers.js';

const appContainer = document.getElementById('app-container');

export async function loadMenu(page) {
  try {
    const templateResponse = await fetch('/pages/templates/menu.html');
    if (!templateResponse.ok) {
      throw new Error('Error loading menu template');
    }

    const templateContent = await templateResponse.text();
    parseAndSetContent(appContainer, templateContent);

    const pageContainer = document.getElementById('page-container');
    const contentResponse = await fetch(page);
    if (!contentResponse.ok) {
      throw new Error('Error loading menu content');
    }

    const pageContent = await contentResponse.text();
    parseAndSetContent(pageContainer, pageContent);

    updateIcons(page);
    const savedLanguage = localStorage.getItem('selectedLanguage') || 'en';
    await changeLanguage(savedLanguage);

    initGlobalValidation(pageContainer);
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
    return;
  }

  const isGamePage = page.includes('/pages/game/');
  const pageType = page.split('/').pop().replace('.html', '');

  let leftIcon = 'bi bi-person-circle';
  let leftHref = '/social';
  let rightIcon = 'bi bi-list';
  let rightHref = '/settings';

  if (pageType === 'auth' || pageType === 'login' || pageType === 'register') {
    leftIcon = 'bi bi-question-circle';
    leftHref = '/auth/privacy';
    rightIcon = 'bi bi-globe';
    rightHref = '/modal-languages';
  } else if (isGamePage) {
    leftIcon = 'bi bi-arrow-left';
    leftHref = '/auth';
    rightIcon = 'bi bi-pause';
    rightHref = '/modal-pause';
  } else if (pageType === 'social') {
    leftIcon = 'bi bi-joystick';
    leftHref = '/';
    rightIcon = 'bi bi-list';
    rightHref = '/settings';
  } else if (pageType === 'settings') {
    leftIcon = 'bi bi-person-circle';
    leftHref = '/social';
    rightIcon = 'bi bi-joystick';
    rightHref = '/';
  }

  leftButton.className = leftIcon;
  leftButton.parentElement.setAttribute('href', leftHref);
  rightButton.className = rightIcon;
  rightButton.parentElement.setAttribute('href', rightHref);
}
