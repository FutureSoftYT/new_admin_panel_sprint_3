# Movies Admin / API - Docker Setup

## Description

This repository contains an API for accessing information about movies and also has default django admin dashboard to
manage movies. The API is designed to be run using Docker
containers for easy deployment and management.

## Setup

#### 1. Clone the repository:

   ```bash
   git clone https://github.com/FuturesoftYT/new_admin_panel_sprint_2.git
   cd new_admin_panel_sprint_2
   ```

#### 2. Configure Environment Variables:

- Locate the `/etc/environs` directory.
- Rename `django.env.example` to `django.env`.
- Rename `postgres.env.example` to `postgres.env`.
- Rename `etl.env.example` to `etl.env`.
- Edit the `django.env`, `etl.env` and `postgres.env` files, providing the required values for the environment variables.

**Variables in `django.env`:**

|      Variable       | Description                                                      |
|:-------------------:|------------------------------------------------------------------|
| `POSTGRES_DATABASE` | PostgreSQL database name                                         |
|   `POSTGRES_USER`   | PostgreSQL username                                              |
| `POSTGRES_PASSWORD` | PostgreSQL password                                              |
|   `POSTGRES_HOST`   | PostgreSQL service host                                          |
|   `POSTGRES_PORT`   | PostgreSQL service port                                          |
|       `DEBUG`       | Django admin mode (True/False)                                   |
|    `SECRET_KEY`     | Django admin secret key (random string used for data encryption) |
|   `ALLOWED_HOSTS`   | Allowed hosts (leave empty for default: localhost and 127.0.0.1) |

**Variables in `postgres.env`:**

|      Variable       | Description              |
|:-------------------:|--------------------------|
|    `POSTGRES_DB`    | PostgreSQL database name |
|   `POSTGRES_USER`   | PostgreSQL username      |
| `POSTGRES_PASSWORD` | PostgreSQL password      |

#### 3. Build and Start Docker Containers:

   ```bash
   docker-compose build
   docker-compose up -d
   ```

#### 4. Access the API and Admin Panel:

- Admin Panel: [http://127.0.0.1/admin](http://127.0.0.1/admin)

  **API Endpoints:**

    - Movies: [http://127.0.0.1/api/v1/movies](http://127.0.0.1/api/v1/movies)
    - Movie by ID: [http://127.0.0.1/api/v1/movies/<UUID>](http://127.0.0.1/api/v1/movies/<UUID>)

  *Replace `<UUID>` with the actual UUID of a specific movie.*

## Filling the Database with Data
To populate your PostgreSQL database with example data, execute command below:

 ```bash
 docker exec -it <CONTAINER> psql -U <POSTGRES_USER> -d <POSTGRES_DB> -f /etc/app/movies_database.sql
 ```

Make sure to replace <CONTAINER> with the actual name or container ID of your PostgreSQL container if it's different. Don't forget changing <POSTGRES_USER> and <POSTGRES_DB> too. 

Once the command completes successfully, the database will be filled with example data.

After filling the database with data, you can access the admin dashboard using the provided credentials.

- Username: `admin`
- Password: `admin`

