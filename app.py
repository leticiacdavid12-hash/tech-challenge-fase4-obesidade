import streamlit as st
import pandas as pd
import joblib
import traceback
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title='Preditor de Obesidade - Hospital', layout='wide')

# Sidebar para navegação
st.sidebar.title('Menu Principal')
aba = st.sidebar.radio('Selecione a página:', ['Predição Individual', 'Painel de Insights Médicos'])

if aba == 'Predição Individual':
    st.title('Sistema de Apoio ao diagnóstico')
    st.markdown('Preencha as informações do paciente abaixo para obter a classificação preditiva.')

    # Carregamento do modelo/pipeline
    @st.cache_resource
    def load_model():
        return joblib.load('models/modelo_obesidade.pkl')

    model = load_model()

    # Formulário de entrada
    with st.form('form_predicao'):
        col1, col2, col3 = st.columns(3)

        with col1:
            genero = st.selectbox('Gênero', ['Feminino', 'Masculino'], index=None, placeholder='Selecione o gênero...')
            idade = st.number_input('Idade', min_value=0, max_value=110, value=None, placeholder='Digite a idade...')
            altura = st.number_input('Altura (m)', min_value=0.0, max_value=2.5, value=None, placeholder='Digite a altura (m)...', step=0.01)
            peso = st.number_input('Peso (kg)', min_value=0.0, max_value=300.0, value=None, placeholder='Digite o peso (kg)...', step=0.1)
            historico_familiar = st.selectbox('Histórico familiar de sobrepeso?', ['Sim', 'Não'], index=None, placeholder='Selecione uma opção...')

        with col2:
            consumo_alimento_calórico = st.selectbox('Consome alimentos calóricos frequentemente?', ['Sim', 'Não'], index=None, placeholder='Selecione uma opção...')
            freq_consumo_vegetais = st.selectbox('Frequência de consumo de vegetais', ['Raramente', 'Às vezes', 'Sempre'], index=None, placeholder='Selecione uma opção...')
            num_refeicoes = st.selectbox('Número de refeições principais por dia', ['1 refeição', '2 refeições', '3 refeições', '4 ou mais refeições'], index=None, placeholder='Selecione uma opção...')
            consumo_entre_refeicoes = st.selectbox('Consumo de alimentos entre as refeições', ['Não consome', 'Consome às vezes', 'Consome frequentemente', 'Consome sempre'], index=None, placeholder='Selecione uma opção...')
            fumante = st.selectbox('É fumante?', ['Sim', 'Não'], index=None, placeholder='Selecione uma opção...')

        with col3:
            consumo_agua = st.selectbox('Consumo diário de água', ['Menos de 1 litro por dia', 'De 1 a 2 litros por dia', 'Mais de 2 litros por dia'], index=None, placeholder='Selecione uma opção...')
            monitora_caloria = st.selectbox('Monitora o consumo de calorias?', ['Sim', 'Não'], index=None, placeholder='Selecione uma opção...')
            freq_atividade_fisica = st.selectbox('Frequência de atividade física semanal', ['Nenhuma', '1 a 2 vezes por semana', '3 a 4 vezes por semana', '5 ou mais vezes por semana'], index=None, placeholder='Selecione uma opção...')
            tempo_tela = st.selectbox('Tempo diário em dispositivos eletrônicos', ['0 a 2 horas por dia', '3 a 5 horas por dia', 'Mais de 5 horas por dia'], index=None, placeholder='Selecione uma opção...')
            consumo_alcool = st.selectbox('Consumo de álcool', ['Não consome', 'Consome às vezes', 'Consome frequentemente', 'Consome sempre'], index=None, placeholder='Selecione uma opção...')

        submit = st.form_submit_button('Gerar Diagnóstico')

    # Processamento e predição
    if submit:

        # Lista de variáveis para verificar se alguma é None
        campos = [genero, idade, altura, peso, historico_familiar, consumo_alimento_calórico, freq_consumo_vegetais, num_refeicoes, consumo_entre_refeicoes, fumante, consumo_agua, monitora_caloria, freq_atividade_fisica, tempo_tela, consumo_alcool]
        
        if None in campos:
            st.error("⚠️ Por favor, preencha todos os campos do formulário antes de gerar o diagnóstico.")
        else:

            # Criar DataFrame com os nomes das colunas idênticos ao treinamento
            dados_entrada = pd.DataFrame({
                'genero': [str(genero)],
                'idade': [int(idade)],
                'altura': [float(altura)],
                'peso': [float(peso)],
                'historico_familiar': [str(historico_familiar)],
                'consumo_alimento_calórico': [str(consumo_alimento_calórico)],
                'freq_consumo_vegetais': [str(freq_consumo_vegetais)],
                'num_refeicoes': [str(num_refeicoes)],  # Forçando string para evitar o erro de iteração
                'consumo_entre_refeicoes': [str(consumo_entre_refeicoes)],
                'fumante': [str(fumante)],
                'consumo_agua': [str(consumo_agua)],
                'monitora_caloria': [str(monitora_caloria)],
                'freq_atividade_fisica': [str(freq_atividade_fisica)],
                'tempo_tela': [str(tempo_tela)],
                'consumo_alcool': [str(consumo_alcool)]
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
            st.markdown("Erro ao processar predição")
            # st.error(f'Erro ao processar predição: {e}')
            # st.code(traceback.format_exc())

elif aba == 'Painel de Insights Médicos':
    st.title('Painel de Insights Estratégicos')
    st.markdown('Este painel apresenta os principais fatores de risco identificados na base de dados para auxiliar a equipe médica em campanhas de prevenção.')

    # Carregar dados para os gráficos
    @st.cache_data
    def get_data():
        return pd.read_csv('data/obesity_cleaned.csv')
        
    df = get_data()

    template = 'streamlit'

    # Função para padronizar layout
    def ajustar_layout(fig):
        fig.update_layout(
            template=template,
            legend=dict(title_text=''),
            margin=dict(l=20, r=20, t=50, b=80),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return fig

    # Criando os grupos por abas
    tab_demo, tab_comport, tab_clinica, tab_ml = st.tabs([
        'Perfil Antropométrico',
        'Perfil Alimentar',
        'Estilo de Vida',
        'Inteligência do Modelo'
    ])

    # Ordenando as categorias de diagnóstico
    diagnostico_ordem = [
        'Abaixo do Peso',
        'Peso Normal',
        'Sobrepeso Nível I',
        'Sobrepeso Nível II',
        'Obesidade Tipo I',
        'Obesidade Tipo II',
        'Obesidade Tipo III'
    ]

    s_n_ordem = ['Sim', 'Não']

    num_refeicoes_ordem = [
        '1 refeição',
        '2 refeições', 
        '3 refeições',
        '4 ou mais refeições'
    ]

    atividade_fisica_ordem = [
        'Nenhuma',
        '1 a 2 vezes por semana',
        '3 a 4 vezes por semana', 
        '5 ou mais vezes por semana'
    ]
    
    # Perfil Antropométrico
    with tab_demo:
        c1, c2 = st.columns(2, gap='large')

        # Gênero por Diagnóstico
        with c1:
            fig1 = px.histogram(
                df, 
                x='diagnostico', 
                color='genero', 
                barmode='stack', 
                barnorm='percent', 
                title='Gênero por Diagnóstico',
                category_orders={
                    'diagnostico': diagnostico_ordem
                },
                labels={
                    'diagnostico': 'Diagnóstico',
                    'genero': 'Gênero'
                })
            fig1.update_layout(yaxis_title='Percentual de Pacientes (%)',)
            st.plotly_chart(ajustar_layout(fig1), use_container_width=True)

            # Histórico Familiar por Diagnóstico
            fig2 = px.histogram(
                df, 
                x='diagnostico', 
                color='historico_familiar', 
                barmode='stack', 
                barnorm='percent', 
                category_orders={
                    'diagnostico': diagnostico_ordem,
                    'historico_familiar': s_n_ordem
                },
            
                title='Histórico Familiar de Sobrepeso por Diagnóstico',
                labels={
                    'diagnostico': 'Diagnóstico',
                    'historico_familiar': 'Histórico Familiar de Sobrepeso'
                })
            fig2.update_layout(yaxis_title='Percentual de Pacientes (%)',)
            st.plotly_chart(ajustar_layout(fig2), use_container_width=True)

            # Idade por Diagnóstico
            fig3 = px.box(
                df, 
                x='diagnostico', 
                y='idade', 
                color='diagnostico', 
                category_orders={
                    'diagnostico': diagnostico_ordem,
                },
                title='Idade por Diagnóstico',
                labels={
                    'diagnostico': 'Diagnóstico',
                    'idade': 'Idade'
                })
            fig3.update_layout(showlegend=False)
            st.plotly_chart(ajustar_layout(fig3), use_container_width=True)

        with c2:

            st.info("""
                    ##### **Principais achados:** \n
                    Os dados sugerem que fatores demográficos e predisposição familiar desempenham papel relevante na progressão da obesidade.\n
                    A combinação de:\n
                    - Histórico familiar positivo\n
                    - Avanço etário\n
                    - Padrões específicos por gênero\n
                    Pode auxiliar na estratificação precoce de risco e priorização de acompanhamento clínico.
                    """)
                    
            st.info("""
                    ##### **Ações clínicas sugeridas:**\n
                    - Intensificar rastreio metabólico em pacientes do sexo mais representado nas classes graves.\n
                    - Considerar fatores hormonais, comportamentais e barreiras específicas por gênero.\n
                    - Avaliar possível atraso na busco por tratamento em determinados grupos.\n
                    - Incluir histórico familiar como marcador precoce de risco.\n
                    - Antecipar intervenções de pacientes com predisposição familiar, mesmo antes do ganho ponderal significativo.\n
                    - Investigar ambiente alimentar e comportamental compartilhado.\n
                    - Monitorar progressão ponderal ao longo do ciclo de vida.\n
                    - Priorizar intervenção precoce em adultos jovens para evitar progressão.\n
                    - Associar rastreio de comorbidades conforme avanço etário.
                    """)

            st.info("""
                    ⚠️ **Observação Importante:** Esses padrões refletem o conjunto de treinamento do modelo e podem influenciar seu comportamento preditivo. Recomenda-se cautela na interpretação em perfis menos representados nos dados.
                    """)

    # Perfil alimentar
    with tab_comport:
        c1, c2 = st.columns(2, gap='large')

        with c1:

            # Consumo de Alimentos Calóricos por Diagnóstico
            fig4 = px.histogram(
                df, 
                x='diagnostico', 
                color='consumo_alimento_calorico', 
                barmode='stack', 
                barnorm='percent', 
                title='Consumo de Alimentos Calóricos por Diagnóstico',
                category_orders={
                    'diagnostico': diagnostico_ordem,
                    'consumo_alimento_calórico': s_n_ordem
                },
                labels={
                    'diagnostico': 'Diagnóstico',
                    'consumo_alimento_calórico': 'Consumo de Alimentos Calóricos'
                })
            fig4.update_layout(yaxis_title='Percentual de Pacientes (%)',)
            st.plotly_chart(ajustar_layout(fig4), use_container_width=True)

            # Frequência de Consumo de Vegetais por Diagnóstico
            fig5 = px.histogram(
                df, 
                x='diagnostico', 
                color='freq_consumo_vegetais', 
                barmode='stack', 
                barnorm='percent', 
                title='Frequência de Consumo de Vegetais por Diagnóstico',
                category_orders={
                    'diagnostico': diagnostico_ordem

                },
                labels={
                    'diagnostico': 'Diagnóstico',
                    'freq_consumo_vegetais': 'Frequência de Consumo de Vegetais'
                })
            fig5.update_layout(yaxis_title='Percentual de Pacientes (%)',)
            st.plotly_chart(ajustar_layout(fig5), use_container_width=True)
       
            # Quantidade de Refeições Principais Diárias por Diagnóstico
            fig6 = px.histogram(
                df, 
                x='diagnostico', 
                color='num_refeicoes', 
                barmode='stack', 
                barnorm='percent', 
                title='Quantidade de Refeições Principais Diárias por Diagnóstico',
                category_orders={
                    'diagnostico': diagnostico_ordem,
                    'num_refeicoes': num_refeicoes_ordem

                },
                labels={
                    'diagnostico': 'Diagnóstico',
                })
            fig6.update_layout(yaxis_title='Percentual de Pacientes (%)',)
            st.plotly_chart(ajustar_layout(fig6), use_container_width=True)

        with c2:

            st.info("""
                    ##### **Principais achados:** \n
                    Os dados sugerem que:\n
                    - A densidade calórica da dieta é fator mais consistente associado à gravidade.\n
                    - O número de refeições isoladamente tem baixa capacidade discriminativa.\n
                    - O consumo autorreferido de vegetais pode não refletir padrão alimentar protetor quando analisado isoladamente.\n
                    """)
                    
            st.info("""
                    ##### **Ações clínicas sugeridas:**\n
                    - Intensificar rastreio metabólico em pacientes do sexo mais representado nas classes graves.\n
                    - Considerar fatores hormonais, comportamentais e barreiras específicas por gênero.\n
                    - Avaliar possível atraso na busco por tratamento em determinados grupos.\n
                    - Incluir histórico familiar como marcador precoce de risco.\n
                    - Antecipar intervenções de pacientes com predisposição familiar, mesmo antes do ganho ponderal significativo.\n
                    - Investigar ambiente alimentar e comportamental compartilhado.\n
                    - Monitorar progressão ponderal ao longo do ciclo de vida.\n
                    - Priorizar intervenção precoce em adultos jovens para evitar progressão.\n
                    - Associar rastreio de comorbidades conforme avanço etário.
                    """)

            st.info("""
                    ⚠️ **Observação Importante:** Esses padrões refletem o conjunto de treinamento do modelo e podem influenciar seu comportamento preditivo. Recomenda-se cautela na interpretação em perfis menos representados nos dados.
                    """)
            
    # Estilo de vida
    with tab_clinica:
        c1, c2 = st.columns(2, gap='large')
        
        with c1:

            # Frequência de Atividade Física por Diagnóstico
            fig7 = px.histogram(
                df, 
                x='diagnostico', 
                color='freq_atividade_fisica', 
                barmode='stack', 
                barnorm='percent', 
                title='Frequência de Atividade Física por Diagnóstico',
                category_orders={
                    'diagnostico': diagnostico_ordem,
                    'freq_atividade_fisica': atividade_fisica_ordem
                },
                labels={
                    'diagnostico': 'Diagnóstico',
                })
            fig7.update_layout(yaxis_title='Percentual de Pacientes (%)',)
            st.plotly_chart(ajustar_layout(fig7), use_container_width=True)

            # Frequência de Consumo de Álcool por Diagnóstico
            fig8 = px.histogram(
                df, 
                x='diagnostico', 
                color='consumo_alcool', 
                barmode='stack', 
                barnorm='percent', 
                title='Frequência de Consumo de Álcool por Diagnóstico',
                category_orders={
                    'diagnostico': diagnostico_ordem

                },
                labels={
                    'diagnostico': 'Diagnóstico',
                })
            fig8.update_layout(yaxis_title='Percentual de Pacientes (%)',)
            st.plotly_chart(ajustar_layout(fig8), use_container_width=True)

            # Fumantes por Diagnóstico
            fig9 = px.histogram(
                df, 
                x='diagnostico', 
                color='fumante', 
                barmode='stack', 
                barnorm='percent', 
                title='Tabagismo por Diagnóstico',
                category_orders={
                    'diagnostico': diagnostico_ordem,
                    'fumante': s_n_ordem
                },
                labels={
                    'diagnostico': 'Diagnóstico',
                })
            fig9.update_layout(yaxis_title='Percentual de Pacientes (%)',)
            st.plotly_chart(ajustar_layout(fig9), use_container_width=True)

        with c2:

            st.info("""
                    ##### **Principais achados:** \n
                    Os dados sugerem que:\n
                    - A atividade física é o fator comportamental mais consistentemente associado à progressão da obesidade.\n
                    - O consumo de álcool, apesar de não apresentar padrão linear evidente, mostrou alta relevância no modelo, possivelmente por interação com outros comportamentos.\n
                    - O tabagismo teve impacto preditivo reduzido no contexto da obesidade.\n
                    """)
                    
            st.info("""
                    ##### **Ações clínicas sugeridas:**\n
                    - Avaliar não apenas prática formal de exercício, mas nível geral de sedentarismo.\n
                    - Estabelecer metas graduais e individualizadas.\n
                    - Monitorar adesão de barreiras comportamentais.\n
                    - Incluir rastreio estruturado de consumo de álcool.\n
                    - Investigar associação de consumo de álcool com ingestão calórica indireta e alimentação fora de rotina.\n
                    - Avaliar possível relação do consumo de álcool com comportamento sedentário.\n
                    - Manter rastreio do consumo de álcool por relevância cardiovascular e metabólica.\n
                    - Não utilizar o consumo de álcool como principal marcador de estratificação de obesidade.
                    """)

            st.info("""
                    ⚠️ **Observação Importante:** Esses padrões refletem o conjunto de treinamento do modelo e podem influenciar seu comportamento preditivo. Recomenda-se cautela na interpretação em perfis menos representados nos dados.
                    """)

    # Inteligência ML
    with tab_ml:
        c1, c2 = st.columns(2, gap='large')

        with c1:
            st.markdown('Este gráfico exibe o peso que o modelo de Machine Learning atribui a cada fator.')

            df_imp = pd.read_csv('data/features_importance.csv')

            fig_imp = px.bar(
                df_imp, x='Peso', y='Variavel', orientation='h', title='Importância das Variáveis para o Diagnóstico', color='Peso', color_continuous_scale='Blues', template=template
            )

            st.plotly_chart(ajustar_layout(fig_imp), use_container_width=True)

        with c2:
            st.info("""
                    #### **Insights**\n
                    O modelo identificou como principais fatores associados ao diagnóstico:\n
                    \n
                    ##### **1. Consumo de álcool**\n
                    Maior relevância preditiva no modelo.\n
                    **Ação sugerida:** Incluir rastreio sistemático de padrão de consumo e investigar possível associação com ingestão calórica indireta e comportamento alimentar.\n
                    \n
                    ##### **2. Frequência de atividade física**\n
                    Associada à progressão dos níveis de obesidade.\n
                    **Ação sugerida:** Reforçar prescrição individualizada de atividade física e acompanhamento de adesão.\n
                    \n
                    ##### **3. Tempo de tela**\n
                    Fator importante na diferenciação entre níveis de obesidade.\n
                    **Ação sugerida:** Avaliar comportamento sedentário e orientar metas graduais de redução do tempo sedentário diário.\n
                    \n
                    ##### **4. Número de refeições**\n
                    Contribuição moderada no modelo.\n
                    **Ação sugerida:** Avaliar padrão alimentar (fracionamento, episódios de belisco, compensações calóricas).
                    """)
            
            st.info("""
                    #### ⚠️ **Observação Clínica**\n
                    A importância das variáveis reflete padrões estatísticos aprendidos pelo modelo e possíveis interações entre fatores. Os achados devem ser utilizados como apoio à decisão clínica, e não como determinantes isolados de causalidade.
                    """)