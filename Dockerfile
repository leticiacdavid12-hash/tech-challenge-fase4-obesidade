# Usa uma imagem leve do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependências primeiro
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o conteúdo do projeto
COPY . .

# Expõe a porta padrão do Streamlit
EXPOSE 8501

# Comando para rodar a aplicação ao iniciar o container
CMD ['streamlit', 'run', 'app.py', '--server.port=8501', '--server.address=0.0.0.0']