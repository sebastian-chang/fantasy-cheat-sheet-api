# Fantasy Cheat Sheet API: A Description

An application that can help aid a user with the selection of a NFL player in their fantasy leagues. A user would be able to see stats from previous seasons.
Graph visualizations of those stats for easy understanding of players performances.  Ideally this could access a player's current season and could work in all leagues for all sports around the world.

## Important Links

- [GitHub API Repo](https://github.com/sebastian-chang/fantasy-cheat-sheet-api)
- [Deployed API](https://fantasy-backend-cheat-sheet.herokuapp.com/)
- [GitHub Repo](https://github.com/sebastian-chang/fantasy-cheat-sheet)
- [Deployed Client](https://sebastian-chang.github.io/fantasy-cheat-sheet/#/)

## Installation

1. Download zip.
2. Unzip the application.
3. Change directories into `fantasy-cheat-sheet-api-master`.
4. Change into your favorite python virual environment.
5. Install all dependencies `pip install` or `pipenv install`.
6. Create a postgres database.
    - Run `psql settings.sql`.
7. Generate and run migrations with `python3 manage.py makemigrations` and `python3 manage.py migrate`.
8. Create super user with `python3 manage.py createsuperuser` follow prompts.
9. Run the server with `python3 manage.py runserver`

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
| POST   | `/qb-stat/`            | `qbstat#create`             | `true`          |

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

![ERD](https://github.com/sebastian-chang/fantasy-cheat-sheet-api/blob/master/public/img/Capstone-ERD.jpg)

---
