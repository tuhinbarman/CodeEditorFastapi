FROM python:3.11.14-alpine3.23

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    build-base

COPY ./backend/requirements.txt /backend/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./backend /backend/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]