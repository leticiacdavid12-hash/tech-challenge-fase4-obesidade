import streamlit as st
import pandas as pd
import joblib
import traceback

# Configuração da página
st.set_page_config(page_title='Preditor de Obesidade - Hospital', layout='wide')

# Carregamento do modelo/pipeline
@st.cache_resource
def load_model():
    return joblib.load('models/modelo_obesidade.pkl')

model = load_model()

st.title('Sistema de Apoio ao Diagnóstico de Obesidade')
st.markdown('Preencha as informações do paciente abaixo para obter a classificação preditiva.')

# Formulário de entrada
with st.form('form_predicao'):
    col1, col2, col3 = st.columns(3)

    with col1:
        genero = st.selectbox('Gênero', ['Feminino', 'Masculino'])
        idade = st.number_input('Idade', min_value=0, max_value=110, value=25)
        altura = st.number_input('Altura (m)', min_value=0.0, max_value=2.5, value=1.70, step=0.01)
        peso = st.number_input('Peso (kg)', min_value=0.0, max_value=300.0, value=70.0, step=0.1)
        historico_familiar = st.selectbox('Histórico familiar de sobrepeso?', ['Sim', 'Não'])

    with col2:
        FAVC = st.selectbox('Consome alimentos calóricos frequentemente?', ['Sim', 'Não'])
        FCVC = st.selectbox('Frequência de consumo de vegetais', ['Raramente', 'Às vezes', 'Sempre'])
        NCP = st.selectbox('Número de refeições principais por dia', ['1 refeição', '2 refeições', '3 refeições', '4 ou mais refeições'])
        CAEC = st.selectbox('Consumo de alimentos entre as refeições', ['Não consome', 'Consome às vezes', 'Consome frequentemente', 'Consome sempre'])
        SMOKE = st.selectbox('É fumante?', ['Sim', 'Não'])

    with col3:
        CH2O = st.selectbox('Consumo diário de água', ['Menos de 1 litro por dia', 'De 1 a 2 litros por dia', 'Mais de 2 litros por dia'])
        SCC = st.selectbox('Monitora o consumo de calorias?', ['Sim', 'Não'])
        FAF = st.selectbox('Frequência de atividade física semanal', ['Nenhuma', '1 a 2 vezes por semana', '3 a 4 vezes por semana', '5 ou mais vezes por semana'])
        TUE = st.selectbox('Tempo diário em dispositivos eletrônicos', ['0 a 2 horas por dia', '3 a 5 horas por dia', 'Mais de 5 horas por dia'])
        CALC = st.selectbox('Consumo de álcool', ['Não consome', 'Consome às vezes', 'Consome frequentemente', 'Consome sempre'])
        MTRANS = st.selectbox('Meio de transporte principal', ['Carro', 'Moto', 'Bicicleta', 'Transporte público', 'A pé'])

    submit = st.form_submit_button('Gerar Diagnóstico')

# Processamento e predição
if submit:
    # Criar DataFrame com os nomes das colunas idênticos ao treinamento
    dados_entrada = pd.DataFrame({
        'genero': [str(genero)],
        'idade': [int(idade)],
        'altura': [float(altura)],
        'peso': [float(peso)],
        'historico_familiar': [str(historico_familiar)],
        'FAVC': [str(FAVC)],
        'FCVC': [str(FCVC)],
        'NCP': [str(NCP)],  # Forçando string para evitar o erro de iteração
        'CAEC': [str(CAEC)],
        'SMOKE': [str(SMOKE)],
        'CH2O': [str(CH2O)],
        'SCC': [str(SCC)],
        'FAF': [str(FAF)],
        'TUE': [str(TUE)],
        'CALC': [str(CALC)],
        'MTRANS': [str(MTRANS)]
    })

    try:
        predicao = model.predict(dados_entrada)
        
        if hasattr(predicao, "__getitem__"):
            resultado_final = str(predicao[0])
        else:
            resultado_final = str(predicao)

        st.subheader('Resultado da Predição')

        # Estilização visual do resultado
        if 'Sobrepeso' in resultado_final:
            cor = 'orange'
        elif 'Obesidade' in resultado_final:
            cor = 'red'
        else:
            cor = 'green'

        st.markdown(f"""
            <div style="padding:20px; border-radius:10px; background-color:rgba(0,0,0,0.1); border-left: 10px solid {cor};">
                <h3 style="color:{cor}; margin:0;">Diagnóstico Predito:</h3>
                <h2 style="color:{cor}; margin:0;">{resultado_final}</h2>
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f'Erro ao processar predição: {e}')
        st.code(traceback.format_exc())