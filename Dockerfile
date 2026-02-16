# 1. Imagem de base do Python
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Instala dependências do sistema necessárias para algumas libs de ML
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# 4. Copia o arquivo de requisitos e instala as bibliotecas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia todo o conteúdo do projeto para dentro do container
COPY . .

# 6. Expõe a porta que o Streamlit usa
EXPOSE 8501

# 7. Comando para rodar a aplicação quando o container iniciar
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.adress=0.0.0.0"]
