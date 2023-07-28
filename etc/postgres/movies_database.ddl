--
-- Создаем схему content
---
CREATE SCHEMA IF NOT EXISTS content;
--
-- Создаем таблицу FilmWork
--
CREATE TABLE IF NOT EXISTS content.film_work
(
    id            uuid PRIMARY KEY,
    title         TEXT         NOT NULL,
    description   TEXT         NULL,
    creation_date DATE,
    rating        FLOAT        NULL,
    type          VARCHAR(255) NOT NULL,
    created       timestamp with time zone,
    modified      timestamp with time zone
);
--
-- Создаем таблицу Genre
--
CREATE TABLE IF NOT EXISTS content.genre
(
    id          uuid PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    description TEXT         NULL,
    created     timestamp with time zone,
    modified    timestamp with time zone
);
--
-- Создаем таблицу Person
--
CREATE TABLE IF NOT EXISTS content.person
(
    id        uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created   timestamp with time zone,
    modified  timestamp with time zone
);
--
-- Создание таблицы GenreFilmwork.
--
CREATE TABLE IF NOT EXISTS content.genre_film_work
(
    id           uuid PRIMARY KEY,
    genre_id     uuid NOT NULL,
    film_work_id uuid NOT NULL,
    created      timestamp with time zone,
    CONSTRAINT fk_inv_film_work_id
        FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE,
    CONSTRAINT fk_inv_genre_id
        FOREIGN KEY (genre_id) REFERENCES content.genre (id) ON DELETE CASCADE
);
--
-- Создание таблицу PersonFilmwork
--
CREATE TABLE IF NOT EXISTS content.person_film_work
(
    id           uuid PRIMARY KEY,
    person_id    uuid         NOT NULL,
    film_work_id uuid         NOT NULL,
    role         VARCHAR(255) NOT NULL,
    created      timestamp with time zone,
    CONSTRAINT fk_inv_film_work_id
        FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE,
    CONSTRAINT fk_inv_person_id
        FOREIGN KEY (person_id) REFERENCES content.person (id) ON DELETE CASCADE
);
--
-- Создаем индекс таблицу genre_film_work что бы нельзя было добавить одного жанра несколько раз к одному фильму
--
CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);
--
-- Создаем индекс что бы нельзя было добавить одного актёра несколько раз к одному фильму с одинакой ролями.
--
CREATE UNIQUE INDEX IF NOT EXISTS film_person_work_idx ON content.person_film_work (film_work_id, person_id, role);
--
-- Создаем индексы для поиска в таблице Film
--
CREATE INDEX IF NOT EXISTS film_work_creation_date_idx ON content.film_work (creation_date);
CREATE INDEX IF NOT EXISTS film_work_rating_idx ON content.film_work (rating);
