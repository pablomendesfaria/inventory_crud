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
COPY src/frontend /app

# Expõe a porta que a aplicação irá rodar
EXPOSE 8501

# Comando para rodar a aplicação
CMD ["poetry", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]