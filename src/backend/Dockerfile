# Usa uma imagem base do Python
FROM python:3.13-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo de dependências para o contêiner
COPY pyproject.toml poetry.lock ./

# Instala o Poetry
RUN pip install poetry

# Instala as dependências do projeto
RUN poetry install --no-root

# Copia o código da aplicação para o contêiner
COPY src/backend /app

# Expõe a porta que a aplicação irá rodar
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]