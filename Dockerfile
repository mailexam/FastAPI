FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY mail.py main.py ./

ENV HTTP_HOST=0.0.0.0
ENV HTTP_PORT=8000

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host $HTTP_HOST --port $HTTP_PORT"]
