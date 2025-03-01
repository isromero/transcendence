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
  // Parse the HTML content
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlString, 'text/html');

  // Clear the container
  container.innerHTML = '';

  // Add all non-script nodes
  Array.from(doc.body.childNodes).forEach(node => {
    if (node.nodeName !== 'SCRIPT') {
      container.appendChild(node.cloneNode(true));
    }
  });

  // Process scripts
  const scripts = Array.from(doc.body.querySelectorAll('script'));

  scripts.forEach(script => {
    if (script.src) {
      const scriptSrc = script.src;
      const scriptType =
        script.type || (scriptSrc.endsWith('.js') ? 'module' : '');

      // ! This is probably not the best solution but it works to force the script to be executed
      // ! In browsers, if a script is added to the DOM and it has a src, it won't be executed
      // ! if was cached, so we need to force a new load of the script
      if (scriptType === 'module') {
        // For ES modules, use a dynamic import with a cache-busting query parameter
        const uuid = crypto.randomUUID(); // Generate a unique ID for the script so it's not cached
        const cacheBuster = `?_cb=${uuid}`;

        const importUrl = scriptSrc.includes('?')
          ? `${scriptSrc}&_cb=${uuid}`
          : `${scriptSrc}${cacheBuster}`;

        // Create a new script element
        const newScript = document.createElement('script');
        newScript.type = 'module';
        newScript.src = importUrl;
        newScript.dataset.originalSrc = scriptSrc; // Store original src for reference
        newScript.dataset.managedBy = 'spa'; // Mark this script as managed by our SPA

        document.body.appendChild(newScript);
      }
    }
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

export function showErrorToast(response) {
  const toastEl = document.getElementById('errorToast');
  let message = '';

  if (typeof response === 'string') {
    message = response;
  } else if (response.error) {
    if (response.error.type === 'validation_error') {
      // Handle form validation errors
      const errors = response.error.fields;
      message = Object.entries(errors)
        .map(
          ([field, msg]) => `${field === '__all__' ? 'Error' : field}: ${msg}`
        )
        .join('\n');
    } else {
      // Handle simple error messages
      message = response.error;
    }
  } else {
    message = 'An unexpected error occurred';
  }

  const messageEl = toastEl.querySelector('.toast-body');
  messageEl.innerHTML = message.replace(/\n/g, '<br>');
  const toast = new bootstrap.Toast(toastEl, { delay: 5000 });
  toast.show();
}
