
const appContainer = document.getElementById('app-container');


async function loadPage(page) {
  try {
    const url = page === '/' ? '/index.html' : `/pages${page}.html`;
    const response = await fetch(url);

    // TODO (samu): Error pages
    if (!response.ok) throw new Error('Página no encontrada');

    const content = await response.text();
    appContainer.innerHTML = content;


    window.history.pushState({ page }, '', page);
  } catch (error) {
    // TODO (samu): Error pages
    appContainer.innerHTML = '<div class="text-center"><h1>Error 404</h1><p>Página no encontrada.</p></div>';
  }
}


document.body.addEventListener('click', (event) => {

  const link = event.target.closest('a.spa-link');
  if (link) {
    event.preventDefault();
    const page = link.getAttribute('href');
    loadPage(page);
  }
});


window.addEventListener('popstate', (event) => {
  const page = event.state?.page || '/';
  loadPage(page);
});


loadPage(window.location.pathname);