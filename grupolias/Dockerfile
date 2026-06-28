FROM python:3.12-slim-bookworm

# Add user that will be used in the container.
RUN useradd wagtail

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip 

# Install the application server.
RUN pip install "gunicorn==25.1.0"

# Install the project requirements.
COPY requirements.txt .
RUN pip install -r ./requirements.txt

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

RUN mkdir -p /app/static \
    && mkdir -p /app/media

RUN chmod +x /app/entrypoint.sh \
    && chown -R wagtail:wagtail /app

# Ejecutar como usuario no privilegiado
USER wagtail

ENTRYPOINT ["sh", "/app/entrypoint.sh"]