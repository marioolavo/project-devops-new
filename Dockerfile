# Imagem base
FROM python:3.12-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o projeto todo
COPY . .

# Variáveis de ambiente do Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Porta exposta
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["flask", "run"]
