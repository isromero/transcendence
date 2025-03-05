import { changeLanguage } from '../utils/languages.js';
import { initGlobalValidation } from '../utils/helpers.js';

const modalContainer = document.getElementById('modal-container');
const modalBackground = document.getElementById('modal-background');
let shouldCloseModal = true; // Variable para controlar si el modal debe cerrarse

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

    // Verificamos si el modal es de tipo end-game o end-game-tournament
    if (page.includes('end-game') || page.includes('end-game-tournament')) {
      shouldCloseModal = false; // No cerramos el modal si es de este tipo
    } else {
      shouldCloseModal = true; // En otros casos, sí cerramos el modal
    }

    const savedLanguage = localStorage.getItem('selectedLanguage') || 'en';
    await changeLanguage(savedLanguage);

    initGlobalValidation(modalContainer);
  } catch (error) {
    console.error('Error loading modal:', error);
  }
}

// Solo cerramos el modal si la variable shouldCloseModal es true
modalBackground.addEventListener('click', event => {
  const clickedModalBackground = event.target.closest('.modal-background');
  if (clickedModalBackground && !event.target.closest('.modal-box') && shouldCloseModal) {
    closeModal();
  }
});

document.addEventListener('click', event => {
  if (event.target.closest('[data-close-modal]') && shouldCloseModal) {
    closeModal();
  }
});
