FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY fixtures ./fixtures
COPY static ./static
ENV PYTHONPATH=/app/src
ENV PORT=8080
CMD exec uvicorn night_clerk.server:app --host 0.0.0.0 --port ${PORT}
