FROM python:3.12

# Устанавливаем зависимости для Poetry и psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && pip install --no-cache-dir poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только poetry.lock и pyproject.toml для кэширования зависимостей
COPY poetry.lock pyproject.toml /app/

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем остальные файлы проекта
COPY . /app/

# Открываем порт Django
EXPOSE 8000

# Указываем команду по умолчанию (но она переопределяется в docker-compose.yaml)
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]


