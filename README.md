FilmService (FastAPI)

FilmService is a REST API built with FastAPI for managing a collection of films.
It integrates with the OMDb API to fetch film data and provides endpoints for storing and retrieving information.
The project is fully dockerized for simple deployment and environment setup.
Features

    Add, update, and delete films.

    Retrieve a list of films with filtering and sorting.

    Retrieve details of a single film.

    Fetch film information from the OMDb API.

    Automatic API documentation with Swagger and ReDoc.

    Microsoft SQL Server integration.

    Ready for deployment with Docker and Docker Compose.

Technologies

    Python 3.10+

    FastAPI

    Uvicorn (ASGI server)

    Pydantic (data validation)

    SQLAlchemy / pyodbc (database access)

    Alembic (migrations, optional)

    OMDb API

    Docker & Docker Compose

    pytest (testing)

Environment Variables

Create a .env file in the root directory:

    DATABASE_URL=mssql+pyodbc://username:password@db:1433/FilmServiceDB?driver=ODBC+Driver+17+for+SQL+Server
    OMDB_API_KEY=your_api_key

Running with Docker

    1. Build and start containers:

    docker-compose up --build

    2. The API will be available at:

    http://127.0.0.1:8000

    3. API documentation:

        Swagger UI: http://127.0.0.1:8000/docs

Testing

    pytest

API Documentation

FastAPI automatically generates OpenAPI specifications.

    Swagger: /docs

