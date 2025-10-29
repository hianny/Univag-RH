FROM python:3.12-slim

# diretório raiz do projeto
WORKDIR /app

# dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copia todo o código
COPY . .

# >>> AQUI: trabalha dentro da pasta UnivagRH <<<
WORKDIR /app/UnivagRH

# porta padrão do Railway
ENV PORT=8080

# start do Gunicorn apontando para tests/app.py
CMD ["sh","-c","gunicorn tests.app:app --workers=1 --timeout=120 --bind 0.0.0.0:${PORT:-8080}"]
