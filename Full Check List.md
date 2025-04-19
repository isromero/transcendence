# Full Check List

## Comprobación subject

### Subject corrección

### General instructions

- Preliminary tests
    - [ ]  Any credentials, API keys, environment variables must be set inside a .env
    any credentials, API keys are available in the git repository and outside of the .env file.
    - [ ]  docker compose file is at the root of the repository
    - [ ]  Run the "docker-compose up --build" command
    - [ ]  500 error, crash, or anything that actually doesn't work within the project scope
- Basic checks
    - [ ]  Website is available
    - [ ]  User can subscribe on the website
    - [ ]  Registered users can log in
    - [ ]  The website is a SPA. User can use Back and Fordward

### The Website

- Security concerns
    - [ ]  Ensure that the website is secure
    - [ ]  Be carefull about TLS. If there is a backend or any other features, it must be available
    - [ ]  Check if there is a database the passwords must be hashed
    - [ ]  Check the server for server-side validation/sanitization on forms and any user input
    - [ ]  Ensure the security measures are properly implemented and thoroughly tested

### The game

- Local game
    - [ ]  You should be able to use this game locally on the same computer using the keyboard
    - [ ]  Each player should be able to utilize a section of the keyboard
    - [ ]  You must also be able to initiate a tournament, and the tournament should offer a match connect local players
- Gameplay
    - [ ]  The game itself must be playable and respect the original Pong game
    - [ ]  The controls must be intuitive or correctly explained
    - [ ]  When a game is over, either a kind of end-game screen is displayed or the game page just exits
- Lags & disconnects
    - [ ]  Unexpected disconnections and lags have to be handled
    - [ ]  The game and the website must not crash when a user is experiencing lags or is disconnected
        - [ ]  Posibles opciones que ofrece el subject para la gestión de esto:
        - [ ]  Pause the game for a defined duration
        - [ ]  Disconnected users can reconnect
        - [ ]  Lagging users can catch up to the match
        - [ ]  And so forth. Any solution is acceptable. The only requirement is: the game should not crush

### General

- Minimal technical requirement
    - [ ]  Backend Framework Module or Ruby
    - [ ]  Database module constraints
    - [ ]  Frontend module or Javascript
    - [ ]  SPA. ← and → buttons
    - [ ]  Latests stable version Google Chrome
    - [ ]  No unhandled errors and no warnings
    - [ ]  Docker → docker-compose up —build
        - [ ]  Rootless mode (ninguno corriendo como root)
        - [ ]  Archivos de ejecución en goinfre /sgoinfre
        - [ ]  No usar volúmenes bind-mount (ruta-host:ruta-cont)
- Game
    - [ ]  Play Pong in browser with same keyboard
    - [ ]  Propose a tournament.
        - [ ]  Clearly display who is playing against whom and order of the players
        - [ ]  Registration system.
        - [ ]  At start tournament, each player must input alias name
        - [ ]  Aliases reset when a new tournament begins
            - [ ]  Modified using Standar User management module (No usado)
        - [ ]  Matchmaking system.
            - [ ]  Organize matchmaking
            - [ ]  Announc next fight
        - [ ]  Same paddle speed.
        - [ ]  capture the essence of original Pong
    
- Security concerns
    - [ ]  Password in database hashed
    - [ ]  Protect SQL injections/XSS
    - [ ]  Enable HTTPS for all aspects (wss, not ws)
    - [ ]  Forms validation and any user input
        - [ ]  Lista de inputs
    - [ ]  API routes protectec
    - [ ]  strong password hashing algorithm
    - [ ]  .env ignored by git

### Modules

- Puntuación
    - [ ]  Framework as backed    +1
    - [ ]  Frontend framework or tookit    +0’5
    - [ ]  Database     +0’5
    - [ ]  User management     +1
    - [ ]  Remote authentication     +1
    - [ ]  Remote players     +1
    - [ ]  GDPR      +0’5
    - [ ]  Monitorin system     +1
    - [ ]  Support on all devices     +0’5
    - [ ]  Expanding Browser Compatibilit     +0’5
    - [ ]  Multiple language support     +1
    - [ ]  Accessibility for visual impaired users     +0’5
    - [ ]  Server-Side Pong an Implementing an API      +1
- Framework as backend
    - [ ]  Django
- Frontend framework or tookit
    - [ ]  Bootstrap toolkit
- Database
    - [ ]  PostgreSQL
- Standard user management, authentication, users across tournaments
    - [ ]  User can subscribe secure
    - [ ]  Login secure
    - [ ]  Unique name to play the tournaments
    - [ ]  Update information
    - [ ]  Upload avatar
    - [ ]  Avatar by default
    - [ ]  Add friends
    - [ ]  See friends status
    - [ ]  Match history
        - [ ]  1v1
        - [ ]  dates
        - [ ]  relevant details
        - [ ]  accesible to logged-in user
    - [ ]  Manage duplicate username
    - [ ]  Manage duplicate emails (Ojo con los @students.42madrid.com)
- Remote authentication
    - [ ]  OAuth with 42
    - [ ]  Manage duplicate username
    - [ ]  Manage duplicate emails (Ojo con los @students.42madrid.com)
    - [ ]  Integrate authentication system
    - [ ]  Obtain the necessary credentials and permissions from the authority to enable a secure login
    - [ ]  User-friendly login and authorization. Adhere best practice and security standards
    - [ ]  Ensure secure exchange of authentication tokens and user information
- Remote players
    - [ ]  Two differents players, separated computer, same website, same game.
    - [ ]  Disconnections
    - [ ]  Lag
- GDPR
    - [ ]  GDPR compliant features
    - [ ]  Anonymization personal data
    - [ ]  Tools for users to manage local data. View, edit or delete personal info stored within the system
    - [ ]  Offer process to reuqest permanent deletion of their accounts
        - [ ]  Associated data
        - [ ]  Ensuring compliance with data regulations
    - [ ]  Clear and transparent communication
- Monitoring system
    - [ ]  Deploy Prometheus to collect metrics about health and performance
    - [ ]  Configure data exporters from different services, databases and infraestruture components
    - [ ]  Custom dashboards and visualizations using Grafana. Real time insights
    - [ ]  Set up alerting rules in Prometheus to detect and respond to critical issues
    - [ ]  Data retention and storage strategies for historical metrics
    - [ ]  Secure authentication and access for Grafana
- Support on all devices
    - [ ]  Works in all types of devices
    - [ ]  Website responsive
        - [ ]  Different screen sizes
        - [ ]  Orientations
        - [ ]  Desktops
        - [ ]  Laptops
        - [ ]  Tablets
        - [ ]  Smartphones
- Expanding Browser Compatibility
    - [ ]  Support additional web browser
    - [ ]  web app functions correctly and display correctly
    - [ ]  Rendering discrepancies
    - [ ]  Mantain usability and functuonality
- Multiple language support
    - [ ]  Three languajes
    - [ ]  Languaje switcher or selector
    - [ ]  Translate essential website content
    - [ ]  Navigate and interact with the website seamlessly
    - [ ]  Language packs or localization libraries to simplify the translation process
    - [ ]  Allow users set default languaje as a default
- Accesibility Visually Impaired Users
    - [ ]  Screen reader and assistive technologies
    - [ ]  Clear and descritive alt text for images
    - [ ]  High-contrast color scheme
    - [ ]  Options for adjusting text size
    - [ ]  Regular updates to meet accesibility standars
- Server-Side Pong an Implementing an API
    - [ ]  Server-side logic to handle gameplay
        - [ ]  ball movement
        - [ ]  scoring
        - [ ]  player interactions
    - [ ]  Create an API with necessary endpoints, allowing usage via web interface
    - [ ]  API endpoint support game initialization, player controls and game state updates
    - [ ]  game responsive, engaging and enjoyable gaming experience
    - [ ]  Integrate server-side Pong game with the web application. Allow users play the game directly on the website