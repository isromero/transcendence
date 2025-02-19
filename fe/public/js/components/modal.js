import { changeLanguage } from '../utils/languages.js';
import { initGlobalValidation } from '../utils/helpers.js';

const modalContainer = document.getElementById('modal-container');
const modalBackground = document.getElementById('modal-background');

export function closeModal() {
  modalContainer.innerHTML = '';
  modalBackground.hidden = true;
}

export async function loadModal(page) {
  try {
    const response = await fetch(page);
    modalBackground.hidden = false;
    const content = await response.text();
    modalContainer.innerHTML = content;

    const savedLanguage = localStorage.getItem('selectedLanguage') || 'en';
    await changeLanguage(savedLanguage);

    initGlobalValidation(modalContainer);
  } catch (error) {
    console.error('Error loading modal:', error);
  }
}

modalBackground.addEventListener('click', event => {
  const clickedModalBackground = event.target.closest('.modal-background');
  if (clickedModalBackground && !event.target.closest('.modal-box')) {
    closeModal();
  }
});

document.addEventListener('click', event => {
  if (event.target.closest('[data-close-modal]')) {
    closeModal();
  }
});
