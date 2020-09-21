# Educational-Store-API: A Description

Something something something.

## Important Links

- [GitHub API Repo](https://github.com/sebastian-chang/fantasy-cheat-sheet-api)
- [Deployed API](https://fantasy-backend-cheat-sheet.herokuapp.com/)
- [GitHub Repo](https://github.com/sebastian-chang/fantasy-cheat-sheet)
- [Deployed Client](https://worldwide-coders.github.io/educational-store/#/)

## Planning Story

- Create the API models and routes.
- Test API connections.
- Build basic front end components.
- Test front end to back end connection.
- Create styling for front end components.
- Test, debug, troubleshoot and debug.
- Reach for stretch goals.
- Use 3rd party API for additional player info.
- Create visualizations for player stats.

## API End Points

| Verb   | URI Pattern            | Controller#Action           | Token Required  |
|--------|------------------------|-----------------------------|-----------------|
| POST   | `/sign-up/`            | `users#signup`              | `false`         |
| POST   | `/sign-in/`            | `users#signin`              | `false`         |
| DELETE | `/sign-out/`           | `users#signout`             | `true`          |
| PATCH  | `/change-pw/`          | `users#changepw`            | `true`          |
| PATCH  | `/update-user`         | `users#updateuser`          | `true`          |
| GET    | `/sheets/`             | `sheets#index`              | `true`          |
| POST   | `/sheets/`             | `sheets#create`             | `true`          |
| GET    | `/sheets/:id`          | `sheets#show`               | `true`          |
| PATCH  | `/sheets/:id`          | `sheets#update`             | `true`          |
| DELETE | `/sheets/:id`          | `sheets#delete`             | `true`          |
| GET    | `/players/`            | `players#index`             | `true`          |
| POST   | `/players/`            | `players#create`            | `true`          |
| GET    | `/players/:id/`        | `players#show`              | `true`          |
| PATCH  | `/players/:id/`        | `players#update`            | `true`          |
| DELETE | `/players/:id/`        | `players#delete`            | `true`          |
| GET    | `/qb-stat/:id/`        | `qbstat#show`               | `true`          |

All data returned from API actions is formatted as JSON.

### Technologies Used

- React
- Javascript
- HTML
- CSS
- Bootstrap
- Django
- SQLAlchemy
- PostgreSQL
- Pandas

### Unsolved Problems

- Creating data science queries to see different visualizations.
- Find more responsive 3rd party sports API

## Images

### ERD

<!-- ![ERD](https://i.imgur.com/iwe6nV4.png) -->

---
