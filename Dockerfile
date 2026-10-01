FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV APP_ENV=development
ENV DB_HOST=localhost
ENV APP_PORT=8080

EXPOSE 8080

CMD ["python", "app.py"]