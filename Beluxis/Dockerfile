FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copiar código
COPY . .

# expor porta (Cloud Run / gunicorn)
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]