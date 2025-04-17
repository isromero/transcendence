import { changeLanguage } from '../pages/languages.js';
import { initGlobalValidation, parseAndSetContent } from '../utils/helpers.js';

const modalContainer = document.getElementById('modal-container');
const modalBackground = document.getElementById('modal-background');
let shouldCloseModal = true; // Variable to control if the modal should be closed

export function closeModal() {
  modalContainer.innerHTML = '';
  modalBackground.hidden = true;
}

export async function loadModal(page) {
  try {
    const response = await fetch(page);

    modalBackground.hidden = false;

    const content = await response.text();
    parseAndSetContent(modalContainer, content);

    // Check if the modal is of type end-game or end-game-tournament
    if (page.includes('end-game') || page.includes('end-game-tournament')) {
      shouldCloseModal = false; // Do not close the modal if it is of this type
    } else {
      shouldCloseModal = true; // In other cases, close the modal
    }

    const savedLanguage = localStorage.getItem('selectedLanguage') || 'en';
    await changeLanguage(savedLanguage);

    initGlobalValidation(modalContainer);
  } catch (error) {
    console.error('Error loading modal:', error);
  }
}

// Event delegation for language changes and modal closing
modalContainer.addEventListener('click', async event => {
  const button = event.target.closest('button');
  if (!button) {
    return;
  }

  // Handle language changes
  const lang = button.dataset.language;
  if (lang) {
    await changeLanguage(lang);
    if (shouldCloseModal) {
      closeModal();
    }
  }

  // Handle modal closing
  if (button.hasAttribute('data-close-modal') && shouldCloseModal) {
    closeModal();
  }
});

// Close modal when clicking outside
modalBackground.addEventListener('click', event => {
  const clickedModalBackground = event.target.closest('.modal-background');
  if (
    clickedModalBackground &&
    !event.target.closest('.modal-box') &&
    shouldCloseModal
  ) {
    closeModal();
  }
});
