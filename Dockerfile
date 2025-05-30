# Usando uma imagem oficial do Python
FROM python:3.12-slim

# Definindo o diretório de trabalho dentro do container
WORKDIR /app

RUN pip install poetry
# Copiando os arquivos necessários para a instalação do Poetry e dependências
COPY pyproject.toml poetry.lock ./

# Instalando o Poetry
RUN poetry config virtualenvs.create false && poetry install --no-root 

# Copiando o restante do código
COPY . .

# Comando para rodar a aplicação
CMD ["poetry", "run", "python", "src/main.py"]