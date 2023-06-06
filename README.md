# fast-social-api
## Project Description
This is a comprehensive learning project I created to understand and implement concepts related to REST API design, database management, and deployment with Docker. The main objective was to create a robust FastAPI application that manages users and posts, offering standard CRUD operations.

### Key Features
1. **User Registration & Authentication**: Users can be created with unique emails and hashed passwords. JWT tokens are issued upon successful login, providing user authentication.
2. **Post Management**: Authenticated users can create, read, update, and delete posts. Users can also upvote posts through a dedicated endpoint.
3. **Alembic Migrations**: Alembic is used as a migration tool to create and manage database tables and rows.
4. **Test Suite**: A suite of unit tests have been written to ensure the functionality of the endpoints.
### Technologies Used
1. **FastAPI**: Used to create the API endpoints and handle HTTP requests and responses.
2. **SQLAlchemy**: Used as the ORM to interact with the database. Also implemented SQL table joins.
3. **JWT**: Handles user authentication by creating and validating JWT tokens.
4. **Pytest**: Utilized to write basic unit tests for the application.
5. **Pydantic**: Validated and documented the API using schemas.
6. **Alembic**: Handled database migrations, making it easy to create and modify database tables and rows.
7. **Poetry**: Managed project dependencies and virtual environment.
8. **Docker**: Packaged the application with all its dependencies into a Docker container, ensuring consistent runs across different platforms.
9. **Nginx**: Used here as a reverse proxy to the FastAPI application.
10. **Postman**: Used for testing the API endpoints manually.
11. **pgAdmin and raw SQL**: Utilized for database management and running raw SQL queries for testing purposes.
12. **Git and GitHub**: Version controlled the project and hosted the codebase on GitHub, practicing the basics of git commands and workflows.

### Setup
**Without docker** : 
1. **Clone the repository**
2. `pip install poetry`
3. `poetry install`
4. `poetry shell`
5. **Set the environment variables**: You will need to set variables for DB_USER, DB_PASSWORD, DB_NAME (database) SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES (jwt generation). You can set these variables in your terminal or add them to a .env file at the root of your project
6. **Run the Alembic migrations to create the database**:  tables `alembic upgrade head`
7. **Start the FastAPI server**: `uvicorn app.main:app --reload`

You should now be able to navigate to http://localhost:8000 to see your application running.

**With docker**: 
1. **Clone the repository**.
2. **Build the Docker images**: `docker-compose build`
3. **Set the environment variables**.
4. **Start the Docker containers** `docker-compose up`

You should now be able to navigate to http://localhost to see your application running.
