const appContainer = document.getElementById('app-container');
const menuContainer = document.getElementById('menu-container');
const modalBackground = document.getElementById('modalus-background');
const modalContainer = document.querySelector('#modal-container');

async function loadPage(page) {
  let url;

  if (page === null) {
	console.log("hola desgracia");
	console.log(page);
    return;
  }

  if (page === '/' || page == '/index.html') {
    page = 'menu-auth';
  }

  if (page.includes('menu-')) {
    page = page.replace('menu-', '');
    url = `/pages/menus/${page}.html`;
    console.log(url);
    loadMenu(url);
  } else if (page.includes('game-')) {
    page = page.replace('game-', '');
    url = `/pages/game/${page}.html`;
    loadGame(url);
  } else if (page.includes('modal-')) {
    page = page.replace('modal-', '');
    url = `/components/${page}.html`;
    loadModal(url);
  } else {
    const message = 'not found page: ${url}';
    loadError(404, message);
  }
}

async function loadMenu(page) {
  try {
    const url = page;
    const response = await fetch(url);
    const template = await fetch('/pages/templates/menu.html');

    if (!template.ok) {
      throw new Error('Error loading template or page content');
    }
    const template_content = await template.text();
    appContainer.innerHTML = template_content;
    if (!response.ok) {
      throw new Error('Error loading template or page content');
    }

    const response_content = await response.text();
    const pageContainer = appContainer.querySelector('#page-container');
    if (!pageContainer) {
      throw new Error(
        'Element with ID "page-container" not found in the template'
      );
    }
    pageContainer.innerHTML = response_content;
    //updateIcons(page);
  } catch (error) {
    loadError('?', error.message);
  }
}

async function loadGame(page) {
  try {
    const url = page;
    const template = await fetch('/pages/templates/main.html');
    const response = await fetch(url);

    if (!response.ok) {
      /* TODO(samusanc): here goes an error checker for debug and other stuff, throw
       * exception is a mistake!!!*/
      throw new Error('Game page not found');
    }

    appContainer.innerHTML = await template.text();
    /*
    const content = await response.text();
    appContainer.innerHTML = content;
	*/
  } catch (error) {
    loadError('madre mia willy', error.message);
  }
}

async function loadModal(page) {
  try {
    const url = page;
    console.log(url);
    const response = await fetch(url);

    modalBackground.hidden = false;

    if (!response.ok) {
      throw new Error('Error loading template or page content');
    }

    const response_content = await response.text();
    modalContainer.innerHTML = response_content;
  } catch (error) {
    loadError('willyyyyyy', error.message);
  }
}

async function loadError(page, message) {
  try {
    const url = page;
    const response = await fetch(url);

    if (!response.ok) {
      /* TODO(samusanc): here goes an error checker for debug and other stuff, throw
       * exception is a mistake!!!*/
      throw new Error('Error page not found');
    }

    const content = await response.text();
    pageContainer.innerHTML = content;

    //window.history.pushState({ page }, '', page);
    //updateIcons(page);
  } catch (error) {
    loadError('ay que se quema la casa', error.message);
  }
}

document.body.addEventListener('click', event => {
  const link = event.target.closest('a.spa-link');

  if (link) {
    event.preventDefault();
    const page = link.getAttribute('spa-loader');
    console.log(page);
    loadPage(page);
  }
});

window.addEventListener('popstate', event => {
  console.log('test');
  const page = event.state?.page || '/';
  loadPage(page);
});

loadPage(window.location.pathname);
