
# TIVIT Challenge

Simple API application, solution for take home test for TIVIT Python role.
Application built using FastAPI as core framework for API service, SqlAlchemy as ORM, PostgreSQL for DB, Alembic for migration management and Docker for containerization.


## Code Structure

Core application files are located at ./src folder

./alembic houses alembic configuration file for autogenerating migrations

./doclerfiles houses dockerfile for API and Alembic containers
## Deployment

Docker is expected to be supported and running on host machine.

To deploy this project run at root:

```bash
  docker compose -f docker-compose.yml up -d
```

Necessary images will be downloaded and containers deployed.
Alembic container will apply migrations once postgre container is ready and will stop.

TIVIT container will serve the API at ```localhost:8800```

## API Reference

User openapi url to interact with API
```localhost:8800/docs```

#### Current user

```http
  GET /fake/current_user
```

Get current logged user

#### Get all users

```http
  GET /fake/all
```

Get all existing users - admin role required

#### Get all user roles

```http
  GET /fake/users
```

Get all existing users with "user" role - user role required

#### Get all admin roles

```http
  GET /fake/admins
```

Get all existing users with "admin" role - admin role required

#### Health check

```http
  GET /fake/health
```

Simply returns a json message if application is running and open to receive requests.

#### Generate JWT token

```http
  POST /fake/token
```

Generate Token from OAuth2PasswordRequestForm provided.