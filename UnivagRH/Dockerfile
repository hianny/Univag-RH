# Usa a imagem oficial do Python
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt requirements.txt

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta usada pelo Railway
EXPOSE 8080

# Comando que inicia o servidor Flask via Gunicorn
CMD ["gunicorn", "tests.app:app", "--workers=2", "--timeout=120", "--bind", "0.0.0.0:8080"]
