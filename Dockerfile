# Base image
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Copia os arquivos de requirements e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte
COPY . .

# Expondo a porta da API
EXPOSE 8000

# Comando para iniciar a API com uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]