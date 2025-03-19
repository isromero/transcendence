import { parseAndSetContent } from '../utils/helpers.js';

const appContainer = document.getElementById('app-container');

export async function loadGame(page) {
  try {
    const response = await fetch(page);
    if (!response.ok) {
      throw new Error('Error loading template or page content');
    }

    const responseContent = await response.text();
    parseAndSetContent(appContainer, responseContent);
  } catch (error) {
    console.error('Error loading game:', error.message);
  }
}
