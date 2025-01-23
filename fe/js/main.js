const appContainer = document.getElementById('app-container');

async function loadPage(page) {
  try {
    const url = page === '/' ? '/index.html' : `/pages${page}.html`;
    const response = await fetch(url);

    if (!response.ok) throw new Error('Página no encontrada');

    const content = await response.text();
    appContainer.innerHTML = content;


    window.history.pushState({ page }, '', page);


    updateIcons(page);
  } catch (error) {
    appContainer.innerHTML = '<div class="text-center"><h1>Error 404</h1><p>Página no encontrada.</p></div>';
  }
}


function updateIcons(page) {
  const leftButton = document.querySelector('.btn.position-absolute.bottom-0.start-0 i');
  const rightButton = document.querySelector('.btn.position-absolute.bottom-0.end-0 i');

  if (page === '/login') {

    leftButton.className = 'bi bi-question-circle';
    rightButton.className = 'bi bi-globe'; 
  } else if (page === '/register') {
    
    leftButton.className = 'bi bi-question-circle';
    rightButton.className = 'bi bi-globe'; 
  }
  else if (page === '/') {
    
    leftButton.className = 'bi bi-question-circle';
    rightButton.className = 'bi bi-globe'; 
  }
   else {

    leftButton.className = 'bi bi-person-circle';
    leftButton.parentElement.setAttribute('href', '/profile');
    rightButton.className = 'bi bi-list'; 
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
