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

// * Parse the HTML content and create script elements to be executed
// * This is ultra important to execute the scripts in a SPA
export function parseAndSetContent(container, htmlString) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlString, 'text/html');

  // Empty the current content
  container.innerHTML = '';

  // Transfer all nodes of the parsed content
  Array.from(doc.body.childNodes).forEach(node => {
    container.appendChild(node.cloneNode(true));
  });

  // Search and execute scripts
  const scripts = Array.from(container.querySelectorAll('script'));
  scripts.forEach(script => {
    const newScript = document.createElement('script');
    newScript.async = false; // Ensure scripts are executed in the order they appear
    newScript.type = 'module';
    if (script.src) {
      newScript.src = script.src;
    } else {
      newScript.textContent = script.textContent;
    }
    script.parentNode.replaceChild(newScript, script);
  });
}

// Global validation of forms
export function initGlobalValidation(root = document) {
  // Select all forms within the container we receive (by default, document)
  const forms = root.querySelectorAll('.needs-validation');

  forms.forEach(form => {
    // To avoid re-initializing a form that already has listeners:
    if (!form.dataset.validationInitialized) {
      form.dataset.validationInitialized = 'true';

      form.addEventListener(
        'submit',
        event => {
          event.preventDefault();
          if (!form.checkValidity()) {
            event.stopPropagation();
            form.classList.add('was-validated');
            return;
          }
          // Emit a custom event if it is valid
          form.dispatchEvent(
            new CustomEvent('formValid', { bubbles: true, cancelable: true })
          );
        },
        false
      );
    }
  });
}

export function showSuccessToast(message) {
  const toastEl = document.getElementById('successToast');
  toastEl.querySelector('.toast-body').textContent = message;
  const toast = new bootstrap.Toast(toastEl, { delay: 5000 });
  toast.show();
}
export function showErrorToast(message) {
  const toastEl = document.getElementById('errorToast');
  toastEl.querySelector('.toast-body').textContent = message;
  const toast = new bootstrap.Toast(toastEl, { delay: 5000 });
  toast.show();
}
