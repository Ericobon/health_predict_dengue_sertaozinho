# 🦟 Predição de Hospitalização por Dengue - Healthcare ML

## 🎯 Objetivo

Desenvolver e comparar modelos de Machine Learning para predizer a probabilidade de hospitalização de pacientes com dengue, otimizados para **maximizar Recall** (detectar casos graves).

## 🏥 Contexto Clínico

Em saúde pública, é **crítico** detectar pacientes que precisam de hospitalização. Um **falso negativo** (paciente grave não detectado) pode resultar em complicações graves ou óbito. Portanto, priorizamos:

1. **Recall (Sensitivity)** - Detectar o máximo de casos graves
2. **NPV** - Confiança em resultados negativos  
3. **Precision (PPV)** - Evitar alarmes falsos excessivos
4. **Specificity** - Identificar corretamente não-hospitalizações

---

## 📊 Dataset

- **Arquivo**: `df_dengue_tratado.csv`
- **Registros**: ~33.000 casos de dengue
- **Período**: 2013-2025
- **Região**: Sertãozinho, SP e região
- **Desbalanceamento**: ~1.17% de hospitalizações (classe minoritária)

### Features Principais

#### Demográficas
- Idade, Sexo, Raça
- Município, Estado

#### Clínicas (5 sintomas principais OMS)
- ✅ **FEBRE**: Febre alta (>38.5°C)
- ✅ **MIALGIA**: Dor muscular intensa
- ✅ **CEFALEIA**: Dor de cabeça (retro-orbital)
- ✅ **VOMITO**: Vômito persistente
- ✅ **EXANTEMA**: Erupções cutâneas

#### Sinais de Alarme
- Petéquias, sangramento
- Dor abdominal intensa

#### Comorbidades
- Diabetes, doenças hematológicas, hepáticas, renais

#### Target
- **HOSPITALIZ**: SIM/NÃO (variável a ser prevista)

---

## 🤖 Modelos Avaliados

O projeto compara **4 algoritmos** de ML:

1. **Regressão Logística** - Baseline interpretável
2. **Random Forest** - Ensemble de árvores
3. **XGBoost** - Gradient Boosting otimizado
4. **CatBoost** - Gradient Boosting com categorical features

Todos configurados com:
- **Class Weight Balancing** ou **SMOTE** para desbalanceamento
- **Otimização para Recall** (class_weight='balanced')
- **Threshold ajustável** (padrão 0.5 → otimizado para Recall ≥ 0.85)

---

## 📁 Estrutura do Projeto

```
pi4v10/
├── df_dengue_tratado.csv              # Dataset original
├── dengue_prediction_advanced.ipynb   # Notebook principal (RECOMENDADO)
├── dengue_prediction_analysis.ipynb   # Notebook básico (apenas Logistic Regression)
├── requirements.txt                    # Dependências Python
├── README_DENGUE_ML.md                # Este arquivo
│
├── .claude/                            # Sistema de orquestração
│   ├── config.json
│   ├── prompts/
│   │   ├── orchestrator.md
│   │   ├── healthcare_ml_specialist.md  # Especialista em ML médico
│   │   ├── data_engineer.md
│   │   └── ...
│   └── tasks/
│
└── outputs/ (gerados após execução)
    ├── best_model_*.pkl               # Modelo vencedor
    ├── scaler_dengue.pkl              # Normalizador
    ├── feature_columns.txt            # Lista de features
    ├── best_model_config.json         # Configuração e métricas
    ├── all_models_metrics.csv         # Comparação de todos os modelos
    │
    └── visualizations/
        ├── model_comparison_metrics.png
        ├── confusion_matrices_comparison.png
        ├── roc_curves_comparison.png
        ├── pr_curves_comparison.png
        ├── shap_summary_plot.png
        ├── shap_feature_importance.png
        └── shap_waterfall_example.png
```

---

## 🚀 Como Executar

### 1. Instalação de Dependências

```bash
cd /home/ericobon/insightesfera/PORTFOLIO_ACADEMICO/pi4v10

# Criar ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Executar Análise Completa

```bash
# Abrir Jupyter Notebook
jupyter notebook dengue_prediction_advanced.ipynb
```

**Ou via linha de comando:**

```bash
# Executar todas as células
jupyter nbconvert --to notebook --execute dengue_prediction_advanced.ipynb
```

### 3. Explorar Resultados

Após a execução, os seguintes arquivos serão gerados:

- ✅ **best_model_*.pkl**: Modelo treinado (usar para predições)
- ✅ **best_model_config.json**: Métricas e configuração
- ✅ **all_models_metrics.csv**: Comparação de todos os modelos
- ✅ **Visualizações PNG**: Gráficos de avaliação

---

## 📊 Pipeline de Análise

### 1. EDA (Exploratory Data Analysis)
- Análise temporal (casos por ano/mês)
- Distribuição demográfica
- Análise de sintomas
- Identificação de valores faltantes
- Correlações

### 2. Feature Engineering
- **SINTOMAS_SCORE**: Soma dos 5 sintomas principais
- **COMORBIDADE_SCORE**: Soma de comorbidades
- **TEM_COMORBIDADE**: Flag binária
- **DIAS_SINTOMA_NOTIFIC**: Tempo entre sintomas e notificação
- **FAIXA_ETARIA**: Categorização de idade

### 3. Preparação dos Dados
- Tratamento de valores "IGNORADO" → binário
- One-hot encoding (raça, etc)
- Normalização (StandardScaler)
- Split estratificado 80/20
- **Balanceamento com SMOTE**

### 4. Modelagem
- Treinamento de 4 modelos
- Cross-validation estratificada (5-fold)
- Otimização de hiperparâmetros

### 5. Avaliação Clínica
- Métricas: Sensitivity, Specificity, PPV, NPV, F1, AUC
- Matriz de confusão (análise de FN e FP)
- Curvas ROC e Precision-Recall
- **Likelihood Ratios** (LR+ e LR-)

### 6. Interpretabilidade
- **SHAP values** (global e individual)
- Feature importance
- Waterfall plots (explicação por paciente)

### 7. Threshold Clínico
- Ajuste de threshold para Recall ≥ 0.85
- Trade-off Precision vs Recall

---

## 🎯 Métricas de Sucesso

### Critérios de Aprovação Clínica

✅ **Recall (Sensitivity) ≥ 0.85**  
   - Detecta pelo menos 85% dos casos de hospitalização

✅ **NPV ≥ 0.95**  
   - 95% de confiança em resultados negativos

✅ **FN minimizados**  
   - Poucos pacientes graves não detectados

✅ **Interpretabilidade**  
   - Médicos entendem as decisões do modelo

---

## 🔍 Interpretação de Resultados

### Exemplo de Output Esperado

```
🏆 MODELO VENCEDOR: XGBoost

📊 MÉTRICAS:
   - Sensitivity (Recall): 0.8734 ⭐ (87.34% dos casos detectados)
   - Specificity:          0.9245 (92.45% dos não-casos identificados)
   - PPV (Precision):      0.3421 (34.21% dos alertas são verdadeiros)
   - NPV:                  0.9912 (99.12% de confiança em negativos)
   - ROC-AUC:              0.9456

⚠️ ANÁLISE DE ERROS:
   - Falsos Negativos: 23 pacientes (12.7% dos positivos reais)
   - Falsos Positivos: 542 alertas desnecessários

💡 INTERPRETAÇÃO:
   - O modelo captura 87% dos casos graves
   - 13% dos casos graves não são detectados (FN)
   - Para cada 3 alertas, 1 é verdadeiro (PPV=34%)
   - Quando o modelo diz "não hospitalizar", tem 99% de chance de estar certo (NPV)
```

### Trade-off Clínico

- **Alto Recall**: Detectamos a maioria dos casos graves ✅
- **Precision moderada**: Muitos alarmes falsos, mas **aceitável** em saúde pública
- **NPV alto**: Podemos confiar nos resultados negativos ✅

---

## 🏥 Features Mais Importantes (Esperado)

Com base em literatura médica, esperamos que as features mais importantes sejam:

1. **VOMITO** - Vômito persistente (sinal de alarme)
2. **SINTOMAS_SCORE** - Quantidade de sintomas
3. **IDADE** - Idosos e crianças têm mais risco
4. **COMORBIDADE_SCORE** - Doenças pré-existentes
5. **PETEQUIA** - Sangramento (sinal de alarme crítico)

---

## 📈 Próximos Passos

### 1. Dashboard Flask/Streamlit
- Interface web para predições
- Visualizações interativas
- Upload de novos casos

### 2. API REST (FastAPI)
- Endpoint `/predict` para predições em tempo real
- Integração com sistemas de saúde
- Latência < 50ms

### 3. Deployment
- Docker container
- Cloud deployment (GCP/AWS)
- Monitoring e logging

### 4. Retraining
- Feedback loop com médicos
- Retraining mensal ou quando drift > 10%
- Validação temporal (dados futuros)

---

## ⚠️ Limitações e Considerações

### Limitações

1. **Dados históricos**: Modelo treinado em dados de 2013-2025
2. **Região específica**: Sertãozinho, SP
3. **Desbalanceamento**: Apenas 1.17% de hospitalizações
4. **Valores ignorados**: Muitos dados clínicos "IGNORADO"

### Considerações Éticas

- ✅ **Não substituir decisão médica**: Ferramenta de apoio, não diagnóstico final
- ✅ **Fairness**: Validar desempenho em diferentes subgrupos (gênero, idade)
- ✅ **Explicabilidade**: Usar SHAP para explicar decisões
- ✅ **Privacidade**: HIPAA/LGPD compliance
- ✅ **Monitoring**: Detectar drift e viés

---

## 📚 Referências

### Literatura Médica

1. WHO (2009). "Dengue: Guidelines for diagnosis, treatment, prevention and control"
2. Ministério da Saúde (2016). "Dengue: diagnóstico e manejo clínico - adulto e criança"

### Machine Learning

1. Kuhn, M., & Johnson, K. (2013). "Applied Predictive Modeling"
2. Molnar, C. (2022). "Interpretable Machine Learning"
3. Chawla et al. (2002). "SMOTE: Synthetic Minority Over-sampling Technique"

---

## 👥 Equipe

**Desenvolvido com sistema de orquestração multi-agent:**

- **@orchestrator**: Coordenação geral
- **@healthcare_ml_specialist**: Modelagem e métricas clínicas
- **@data_engineer**: ETL e feature engineering
- **@ml_engineer**: Treinamento e otimização

---

## 📞 Suporte

Para dúvidas ou sugestões:

- 📧 Email: [seu-email]
- 🐛 Issues: [GitHub Issues]
- 📖 Docs: [Link para documentação]

---

**Em saúde, Recall > tudo. É melhor errar por excesso de cuidado!** 🏥
