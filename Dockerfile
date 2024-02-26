# Dockerfile for development
FROM python:3.12-slim-bookworm

WORKDIR /app


COPY . .
RUN apt-get update && apt-get install -y  libmagic-dev
RUN pip install --no-cache-dir -r  requirements_for_linux.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]