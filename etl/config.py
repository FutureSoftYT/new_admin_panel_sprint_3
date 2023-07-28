import os

from dotenv import load_dotenv

load_dotenv()

SCHEMA_CONTENT = 'content'

PERSON_TABLE = 'person'
GENRE_TABLE = 'genre'
FILM_WORK_TABLE = 'film_work'
FILM_WORK_GENRE_M2M_TABLE = 'genre_film_work'
FILM_WORK_PERSON_M2M_TABLE = 'person_film_work'

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

TABLES_DATA = {
    0: (FILM_WORK_TABLE, '', ''),
    1: (PERSON_TABLE, FILM_WORK_PERSON_M2M_TABLE, 'person_id'),
    2: (GENRE_TABLE, FILM_WORK_GENRE_M2M_TABLE, 'genre_id'),
}

DSL = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': os.environ.get('DB_PORT', 5432),
}

# ElasticSearch Index
INDEX_NAME = 'movies'
ES_HOST = os.environ.get('ES_HOST', '127.0.0.1')
ES_PORT = os.environ.get('ES_PORT', 9200)

ES_SETTINGS = {
    "refresh_interval": "1s",
    "analysis": {
        "filter": {
            "english_stop": {
                "type": "stop",
                "stopwords": "_english_"
            },
            "english_stemmer": {
                "type": "stemmer",
                "language": "english"
            },
            "english_possessive_stemmer": {
                "type": "stemmer",
                "language": "possessive_english"
            },
            "russian_stop": {
                "type": "stop",
                "stopwords": "_russian_"
            },
            "russian_stemmer": {
                "type": "stemmer",
                "language": "russian"
            }
        },
        "analyzer": {
            "ru_en": {
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "english_stop",
                    "english_stemmer",
                    "english_possessive_stemmer",
                    "russian_stop",
                    "russian_stemmer"
                ]
            }
        }
    }
}

ES_MAPPINGS = {
    "dynamic": "strict",
    "properties": {
        "id": {
            "type": "keyword"
        },
        "imdb_rating": {
            "type": "float"
        },
        "genre": {
            "type": "keyword"
        },
        "title": {
            "type": "text",
            "analyzer": "ru_en",
            "fields": {
                "raw": {
                    "type": "keyword"
                }
            }
        },
        "description": {
            "type": "text",
            "analyzer": "ru_en"
        },
        "director": {
            "type": "text",
            "analyzer": "ru_en"
        },
        "actors_names": {
            "type": "text",
            "analyzer": "ru_en"
        },
        "writers_names": {
            "type": "text",
            "analyzer": "ru_en"
        },
        "actors": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "id": {
                    "type": "keyword"
                },
                "name": {
                    "type": "text",
                    "analyzer": "ru_en"
                }
            }
        },
        "writers": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "id": {
                    "type": "keyword"
                },
                "name": {
                    "type": "text",
                    "analyzer": "ru_en"
                }
            }
        }
    }
}
