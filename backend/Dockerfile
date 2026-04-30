FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r backend/requirements.txt

EXPOSE 8790

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8790"]
