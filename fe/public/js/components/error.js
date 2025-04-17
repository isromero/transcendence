const appContainer = document.getElementById('app-container');

export function loadErrorPage(errorMessage) {
  const errorHTML = `
        <div class="d-flex justify-content-center align-items-center vh-100">
            <div class="text-center">
                <h1 class="title-principal-styles mb-4">Error</h1>
                <p class="form-secondary-title-color mb-4">${errorMessage}</p>
                <a href="/auth" class="spa-link">
                    <button class="btn login-button bs-primary" style="border-radius: 10px; height: 2.8rem;">
                        Return to Home
                    </button>
                </a>
            </div>
        </div>
    `;

  appContainer.innerHTML = errorHTML;
}
