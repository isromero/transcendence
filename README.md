# transcendence

## Requirements (major/minor modules chosen and more)
https://arc.net/e/059DF97D-3F04-49D1-A61C-EE5878BE8AB6

## Project Setup

### Prerequisites
- Docker and Docker Compose
- Node.js 20.0.0 or higher
- VS Code with recommended extensions (for linting and formatting)
- Black formatter (`pip install black`) if you want to use it locally
- Flake8 (`pip install flake8`) if you want to use it locally

### Development Environment
1. Clone the repository
2. Create environment files in fe/.env and be/.env (see .env.example)
3. Run docker compose build
4. Run docker compose up

## Migrations
We don't use a virtual environment so you will need to run the migrations in the container.

```bash
docker compose run --rm be python manage.py makemigrations
docker compose run --rm be python manage.py migrate
```


### Services
The services will be available at:
- Backend: http://localhost:8000
- Frontend: http://localhost:3001
- Database: http://localhost:5432

### Linting and Formatting VS Code
Intall the following extensions:
- ESLint
- Prettier
- Black Formatter -> ms-python.black-formatter
- Flake8 -> ms-python.flake8 (you will need to install flake8 locally)

### Frontend Code Quality Tools inside fe/
#### ESLint
- Lints JavaScript, HTML and CSS files
- Run: `npm run lint`
- Fix: `npm run lint:fix`

#### Prettier
- Formats JavaScript, HTML and CSS files
- Run: `npm run format`
- Check: `npm run format:check`

#### Combined Commands
- Check all: `npm run check`
- Fix all: `npm run fix`

### Backend Code Quality Tools inside be/
#### Black (Formatter)
- Format all files: `black .`
- Check format: `black . --check`

#### Flake8 (Linter)
- Check all files: `flake8`

## Project Structure

- be/
  - apps/ Contains all the applications
    - core/ Contains all the core modules
  - config/ Contains all the configuration files

- fe/
  - assets/ Contains all the assets
    - fonts/ Contains all the fonts
    - images/ Contains all the images
  - css/ Contains all the CSS files
    - styles.css Contains the main styles file
    - pages/ Contains all the pages
    - components/ Contains all the components
  - js/ Contains all the JavaScript files
    - main.js Contains the main JavaScript file
    - components/ Contains all the components
    - pages/ Contains all the pages
    - services/ Contains all the services (API calls)
    - utils/ Contains all the utility functions
  - index.html/ Contains the main HTML file
  - jsconfig.json/ Contains the JavaScript configuration file
  - eslint.config.js/ Contains the ESLint configuration file
  - .prettierrc Contains the Prettier configuration file

## Commits and branch names

In this project, we follow the Conventional Commits specification for structuring our commit messages and branch names. It enables automated tools and processes to analyze and generate release notes, changelogs, and versioning information. For more info on Conventional Commits, visit <https://www.conventionalcommits.org/en/v1.0.0/>

### Commit Message Format

Each commit message follows a specific format:

```code
<type>(<scope>): <subject>
```

`<type>`: Describes the purpose or nature of the commit. It can be one of the following values: `feat, fix, docs, style, refactor, test, chore, perf`.

`<scope>` (optional): Specifies the part of the project or component the commit affects. It can be a module, file, or a broader area of impact.

`<subject>`: A concise and clear description of the change. It should be written in the imperative mood, starting with a capital letter and without ending punctuation.

#### Examples of valid commit messages

```code
fix(authentication): Resolve login issue on Safari
feat(files): Add file upload feature
perf: Update dependencies to latest versions
```

### Branch Names

When creating branch names, we follow the same conventions as commit messages to maintain consistency and clarity

#### Examples of branch names

```code
feat/file-upload
fix/authentication-safari-login-issue
perf/bump-dependencies
```