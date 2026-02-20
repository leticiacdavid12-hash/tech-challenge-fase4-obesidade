import pandas as pd
import sqlite3
import os

# Caminho dos arquivos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(BASE_DIR, 'data', 'Obesity.csv')
db_path = os.path.join(BASE_DIR, 'data', 'hospital.db')

print(f"Buscando arquivo em: {csv_path}")
try:
    df = pd.read_csv(csv_path)

    conn = sqlite3.connect(db_path)
    df.to_sql('pacientes', conn, if_exists='replace', index=False)
    conn.close()

    print(f"Banco de dados criado em: {db_path}")
    print(f"Total de registros: {len(df)}")

except FileNotFoundError:
    print(f"ERRO: O arquivo 'Obesity.csv' não foi encontrado na pasta 'data'.")
