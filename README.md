# Tech Challenge - Fase 4: Predição de Obesidade

## Visão Geral
Este projeto for desenvolvido para auxiliar a equipe médica de um hospital na identificação precoce e classificação dos níveis de obesidade em pacientes, utilizando Machine Learning.

## Acesso Rápido
- **Aplicação Web:** https://tech-challenge-fase4-obesidade-2026.streamlit.app/
- **Vídeo de Apresentação:** https://youtube.com/watch?v=AgbXypB6z0s&feature=shared

## Tecnologias e Arquitetura
* **Linguagem:** Python 3.11
* **Machine Learning:** Scikit-Learn (Pipeline com OrdinalEncoder e StandardScaler)
* **Interface:** Streamlit (com abas de predição e dashboard analítico)
* **Persistência:** Joblib para o modelo e SQLite para armazenamento de logs/dados.
* **Infraestrutura:** Docker (arquivos de configuração inclusos para reprodutibilidade local).

## Estrutura do Projeto
- `data/`: Base Obesity.csv e banco hospital.db.
- `models/`: Modelo serializado .pkl.
- `notebooks/`: Processo completo de EDA, limpeza, pré-processamento e treinamento.
- `src/`: Scripts de suporte.
