'''
Dashboard Flask - Projeto Integrador IV (PI4v10) - Dengue Sertãozinho

📊 DADOS:
- Dataset: df_dengue_tratado.csv (33.319 casos reais de Sertãozinho, 2000-2025)
- Uso: Estatísticas descritivas e visualizações

🤖 MODELO:
- Arquivo: models/modelo_reglog_otimizado.pkl
- Tipo: Regressão Logística otimizada com Optuna
- Treinamento: 15/11/2025 13:39:45
- Features: 14 (selecionadas via Feature Importance + Correlação + Chi²)
- Balanceamento: SMOTE aplicado no conjunto de treino
- Métricas (conjunto de teste):
  * Sensitivity (Recall): 43.64%
  * Specificity: 74.02%
  * NPV: 98.87%
  * AUC: 62.95%

💡 FUNCIONAMENTO:
- Usuário fornece 5 sintomas: FEBRE, MIALGIA, CEFALEIA, VOMITO, EXANTEMA
- Sistema calcula SEVERITY_SCORE e preenche outras 9 features com valores padrão
- Modelo faz predição com as 14 features completas
'''

from flask import Flask, render_template, jsonify, request
import pandas as pd
import joblib
import numpy as np
import os

app = Flask(__name__)

# --- Configurações do Modelo ---
MODEL_PATH = "models/modelo_reglog_otimizado.pkl"
SCALER_PATH = "models/scaler_final.pkl"

# Features esperadas pelo modelo (14 features selecionadas)
MODEL_FEATURES = [
    'DIAS_SINTOMA_NOTIFIC_TEMP', 'TRIMESTRE', 'MES', 'DIAS_SINTOMA_NOTIFIC',
    'TEM_COMORBIDADE', 'NU_ANO', 'QTD_IGNORADOS', 'SEVERITY_SCORE',
    'IDADE', 'ANO', 'HEPATOPAT_BIN', 'COMORBIDADE_SCORE',
    'DIABETES_BIN', 'RENAL_BIN'
]

# Features coletadas do usuário (5 sintomas principais)
USER_INPUT_FEATURES = ['FEBRE', 'MIALGIA', 'CEFALEIA', 'VOMITO', 'EXANTEMA']

# --- Carregamento de Dados ---

# 1. Dataset de Sertãozinho (para estatísticas e visualizações)
print("Carregando dataset de Sertãozinho para estatísticas...")
try:
    df_stats = pd.read_csv("data/df_dengue_tratado.csv")
    df_stats["DT_NOTIFIC"] = pd.to_datetime(df_stats["DT_NOTIFIC"])
    df_stats["DT_SIN_PRI"] = pd.to_datetime(df_stats["DT_SIN_PRI"])
    df_stats["NU_ANO"] = df_stats["DT_NOTIFIC"].dt.year
    print(f"   ✓ Dataset de estatísticas carregado: {len(df_stats):,} registros")
except FileNotFoundError:
    print("ERRO: df_dengue_tratado.csv não encontrado.")
    df_stats = pd.DataFrame()

# 2. Modelo Preditivo
print(f"Carregando modelo preditivo de {MODEL_PATH}...")
try:
    model = joblib.load(MODEL_PATH)
    print(f"   ✓ Modelo carregado: {type(model).__name__}")
except Exception as e:
    print(f"ERRO ao carregar o modelo: {e}")
    model = None

# --- Rotas da Aplicação ---

@app.route("/")
def index():
    '''Renderiza a página principal.'''
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    '''Renderiza o dashboard interativo.'''
    return render_template("dashboard.html")

# --- API para Estatísticas (usa df_stats) ---

@app.route("/api/data/summary")
def data_summary():
    '''Retorna um resumo dos dados REAIS de Sertãozinho.'''
    if df_stats.empty:
        return jsonify({"error": "Dados de estatísticas não carregados"}), 500
        
    total_casos = len(df_stats)
    casos_hospitalizados = len(df_stats[df_stats["HOSPITALIZ"] == "SIM"])
    taxa_hospitalizacao = (casos_hospitalizados / total_casos) * 100 if total_casos > 0 else 0
    
    summary = {
        "total_casos": total_casos,
        "casos_hospitalizados": casos_hospitalizados,
        "taxa_hospitalizacao": round(taxa_hospitalizacao, 2),
        "idade_media": round(df_stats["IDADE"].mean(), 1),
        "anos_cobertura": f"{df_stats['NU_ANO'].min()} - {df_stats['NU_ANO'].max()}"
    }
    return jsonify(summary)

@app.route("/api/data/casos_por_ano")
def casos_por_ano():
    '''Retorna dados de casos por ano do dataset de Sertãozinho.'''
    if df_stats.empty:
        return jsonify({"error": "Dados de estatísticas não carregados"}), 500
    casos_ano = df_stats["NU_ANO"].value_counts().sort_index()
    data = {
        "anos": casos_ano.index.tolist(),
        "casos": casos_ano.values.tolist()
    }
    return jsonify(data)

@app.route("/api/data/casos_por_mes")
def casos_por_mes():
    '''Retorna dados de casos por mês do dataset de Sertãozinho.'''
    if df_stats.empty:
        return jsonify({"error": "Dados de estatísticas não carregados"}), 500
    df_stats["MES_NOTIFIC"] = df_stats["DT_NOTIFIC"].dt.month
    casos_mes = df_stats["MES_NOTIFIC"].value_counts().sort_index()
    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    data = {
        "meses": [meses[i-1] for i in casos_mes.index],
        "casos": casos_mes.values.tolist()
    }
    return jsonify(data)

@app.route("/api/data/distribuicao_sexo")
def distribuicao_sexo():
    '''Retorna dados de distribuição por sexo.'''
    if df_stats.empty:
        return jsonify({"error": "Dados de estatísticas não carregados"}), 500
    sexo_counts = df_stats['CS_SEXO'].value_counts()
    data = {
        "labels": sexo_counts.index.tolist(),
        "values": sexo_counts.values.tolist()
    }
    return jsonify(data)

@app.route("/api/data/fenomeno_climatico")
def fenomeno_climatico():
    '''Retorna dados de distribuição por fenômeno climático.'''
    if df_stats.empty:
        return jsonify({"error": "Dados de estatísticas não carregados"}), 500
    fenomeno_counts = df_stats['FENOMENO'].value_counts()
    data = {
        "labels": fenomeno_counts.index.tolist(),
        "values": fenomeno_counts.values.tolist()
    }
    return jsonify(data)

@app.route("/api/data/hospitalizacao_por_idade")
def hospitalizacao_por_idade():
    '''Retorna dados de hospitalização por faixa etária.'''
    if df_stats.empty:
        return jsonify({"error": "Dados de estatísticas não carregados"}), 500
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 120]
    labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '90+']
    df_stats['faixa_etaria'] = pd.cut(df_stats['IDADE'], bins=bins, labels=labels, right=False)
    
    hosp_por_idade = df_stats[df_stats['HOSPITALIZ'] == 'SIM']['faixa_etaria'].value_counts().sort_index()
    total_por_idade = df_stats['faixa_etaria'].value_counts().sort_index()
    
    data = {
        "faixas": total_por_idade.index.tolist(),
        "hospitalizados": hosp_por_idade.reindex(total_por_idade.index, fill_value=0).values.tolist(),
        "total": total_por_idade.values.tolist()
    }
    return jsonify(data)

@app.route("/api/data/distribuicao_raca")
def distribuicao_raca():
    '''Retorna dados de distribuição por raça.'''
    if df_stats.empty:
        return jsonify({"error": "Dados de estatísticas não carregados"}), 500
    raca_counts = df_stats['CS_RACA'].value_counts()
    data = {
        "labels": raca_counts.index.tolist(),
        "values": raca_counts.values.tolist()
    }
    return jsonify(data)

@app.route('/api/data/filtered', methods=['POST'])
def get_filtered_data():
    '''Retorna dados filtrados para o dashboard.'''
    if df_stats.empty:
        return jsonify({"error": "Dados de estatísticas não carregados"}), 500
    filters = request.json
    
    filtered_df = df_stats.copy()
    
    if filters.get('anoInicial'):
        filtered_df = filtered_df[filtered_df['NU_ANO'] >= int(filters['anoInicial'])]
    if filters.get('anoFinal'):
        filtered_df = filtered_df[filtered_df['NU_ANO'] <= int(filters['anoFinal'])]
    if filters.get('fenomeno'):
        filtered_df = filtered_df[filtered_df['FENOMENO'] == filters['fenomeno']]
    if filters.get('sexo'):
        filtered_df = filtered_df[filtered_df['CS_SEXO'] == filters['sexo']]

    # Recalcular todos os dados para os gráficos com base no df filtrado
    # Summary
    total_casos = len(filtered_df)
    casos_hospitalizados = len(filtered_df[filtered_df["HOSPITALIZ"] == "SIM"])
    taxa_hospitalizacao = (casos_hospitalizados / total_casos) * 100 if total_casos > 0 else 0
    idade_media = round(filtered_df["IDADE"].mean(), 1) if total_casos > 0 else 0

    summary = {
        "total_casos": total_casos,
        "casos_hospitalizados": casos_hospitalizados,
        "taxa_hospitalizacao": round(taxa_hospitalizacao, 2),
        "idade_media": idade_media
    }

    # Casos por Ano
    casos_ano = filtered_df["NU_ANO"].value_counts().sort_index()
    casos_por_ano_data = {
        "anos": casos_ano.index.tolist(),
        "casos": casos_ano.values.tolist()
    }

    # Distribuição por Sexo
    sexo_counts = filtered_df['CS_SEXO'].value_counts()
    distribuicao_sexo_data = {
        "labels": sexo_counts.index.tolist(),
        "values": sexo_counts.values.tolist()
    }

    # Casos por Mês
    filtered_df["MES_NOTIFIC"] = filtered_df["DT_NOTIFIC"].dt.month
    casos_mes = filtered_df["MES_NOTIFIC"].value_counts().sort_index()
    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    casos_por_mes_data = {
        "meses": [meses[i-1] for i in casos_mes.index],
        "casos": casos_mes.values.tolist()
    }

    # Fenômeno Climático
    fenomeno_counts = filtered_df['FENOMENO'].value_counts()
    fenomeno_climatico_data = {
        "labels": fenomeno_counts.index.tolist(),
        "values": fenomeno_counts.values.tolist()
    }

    # Hospitalização por Idade
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 120]
    labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '90+']
    filtered_df['faixa_etaria'] = pd.cut(filtered_df['IDADE'], bins=bins, labels=labels, right=False)
    hosp_por_idade = filtered_df[filtered_df['HOSPITALIZ'] == 'SIM']['faixa_etaria'].value_counts().sort_index()
    total_por_idade = filtered_df['faixa_etaria'].value_counts().sort_index()
    hospitalizacao_idade_data = {
        "faixas": total_por_idade.index.tolist(),
        "hospitalizados": hosp_por_idade.reindex(total_por_idade.index, fill_value=0).values.tolist(),
        "total": total_por_idade.values.tolist()
    }

    # Distribuição por Raça
    raca_counts = filtered_df['CS_RACA'].value_counts()
    distribuicao_raca_data = {
        "labels": raca_counts.index.tolist(),
        "values": raca_counts.values.tolist()
    }

    return jsonify({
        "summary": summary,
        "casosPorAno": casos_por_ano_data,
        "distribuicaoSexo": distribuicao_sexo_data,
        "casosPorMes": casos_por_mes_data,
        "fenomenoClimatico": fenomeno_climatico_data,
        "hospitalizacaoIdade": hospitalizacao_idade_data,
        "racaDistribution": distribuicao_raca_data
    })

# --- API para Predição (usa o modelo retreinado) ---

@app.route("/api/predict", methods=["POST"])
def predict():
    '''
    Endpoint para predição do modelo de Regressão Logística.

    Modelo: Modelo otimizado com 14 features
    Input do usuário: 5 sintomas principais (FEBRE, MIALGIA, CEFALEIA, VOMITO, EXANTEMA)
    Outras features: Preenchidas com valores médios/padrão
    '''
    if model is None:
        return jsonify({"error": "Modelo não carregado"}), 500

    try:
        data = request.json

        # Coletar os 5 sintomas do usuário
        febre = 1 if data.get("febre", "NÃO").upper() == "SIM" else 0
        mialgia = 1 if data.get("mialgia", "NÃO").upper() == "SIM" else 0
        cefaleia = 1 if data.get("cefaleia", "NÃO").upper() == "SIM" else 0
        vomito = 1 if data.get("vomito", "NÃO").upper() == "SIM" else 0
        exantema = 1 if data.get("exantema", "NÃO").upper() == "SIM" else 0

        # Criar array com as 14 features esperadas pelo modelo
        # Ordem: DIAS_SINTOMA_NOTIFIC_TEMP, TRIMESTRE, MES, DIAS_SINTOMA_NOTIFIC, TEM_COMORBIDADE,
        #        NU_ANO, QTD_IGNORADOS, SEVERITY_SCORE, IDADE, ANO, HEPATOPAT_BIN, COMORBIDADE_SCORE, DIABETES_BIN, RENAL_BIN

        # Calcular SEVERITY_SCORE baseado nos sintomas
        severity = exantema * 1 + vomito * 3 + mialgia * 1 + cefaleia * 1 + febre * 1

        # Valores padrão/médios para as outras features
        X_input = np.array([[
            2,          # DIAS_SINTOMA_NOTIFIC_TEMP (média: 2 dias)
            1,          # TRIMESTRE (1 = verão, período de maior incidência)
            3,          # MES (março, pico de casos)
            2,          # DIAS_SINTOMA_NOTIFIC
            0,          # TEM_COMORBIDADE (0 = não tem)
            2024,       # NU_ANO
            0,          # QTD_IGNORADOS
            severity,   # SEVERITY_SCORE (calculado baseado nos sintomas)
            35,         # IDADE (média: 35 anos)
            2024,       # ANO
            0,          # HEPATOPAT_BIN (0 = não)
            0,          # COMORBIDADE_SCORE
            0,          # DIABETES_BIN (0 = não)
            0           # RENAL_BIN (0 = não)
        ]])

        # Fazer predição
        prediction_proba = model.predict_proba(X_input)
        prob_hospitalizacao = prediction_proba[0][1]  # Probabilidade da classe 1 (SIM)

        return jsonify({"probabilidade_hospitalizacao": round(prob_hospitalizacao * 100, 2)})

    except Exception as e:
        import traceback
        return jsonify({
            "error": f"Erro na predição: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
