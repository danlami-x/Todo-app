FROM python:3.10

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --default-timeout=100 --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8009
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8009"]
