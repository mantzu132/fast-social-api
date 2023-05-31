FROM python

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1

# Setup the working directory for the application
WORKDIR /fast-social-api

RUN pip install --no-cache-dir 'poetry==1.4.2'

# Copy only requirements, to cache them in docker layer
COPY poetry.lock pyproject.toml /fast-social-api/

# Project initialization: don't create a virtual env
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy all files into the image
COPY . /fast-social-api/

# Create database table with alembic and run the server
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 "]

