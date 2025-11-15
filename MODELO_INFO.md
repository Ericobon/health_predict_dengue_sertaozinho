# 📊 Informações do Modelo e Dados - Dashboard Dengue

## 🎯 Entenda a Diferença

### 📈 DATASET DE ESTATÍSTICAS (33.319 casos)
**Arquivo**: `data/df_dengue_tratado.csv`

**Descrição**: Dataset REAL de notificações de dengue em Sertãozinho-SP (2000-2025)

**Uso no Dashboard**:
- ✅ Estatísticas gerais (total de casos, hospitalizações, etc.)
- ✅ Gráficos de análise exploratória
- ✅ Distribuições temporais, demográficas e climáticas

**Características**:
- Total: 33.319 registros
- Período: 2000-2025
- Taxa de hospitalização REAL: ~1.17% (dados desbalanceados)
- Região: Sertãozinho-SP

---

### 🤖 MODELO DE MACHINE LEARNING
**Arquivo**: `models/modelo_reglog_otimizado.pkl`

**Descrição**: Modelo de Regressão Logística treinado para predizer hospitalização

**Treinamento**:
- **Data**: 15/11/2025 às 13:39:45
- **Algoritmo**: Logistic Regression (Optuna)
- **Origem dos dados**: df_dengue_tratado.csv (33.319 casos)
- **Balanceamento**: SMOTE aplicado APENAS no conjunto de TREINO
- **Features**: 14 selecionadas (de 23 originais)
- **Split**: 80% treino / 20% teste (estratificado)

**Features Utilizadas (14)**:
1. DIAS_SINTOMA_NOTIFIC_TEMP
2. TRIMESTRE
3. MES
4. DIAS_SINTOMA_NOTIFIC
5. TEM_COMORBIDADE
6. NU_ANO
7. QTD_IGNORADOS
8. SEVERITY_SCORE ⭐
9. IDADE
10. ANO
11. HEPATOPAT_BIN
12. COMORBIDADE_SCORE
13. DIABETES_BIN
14. RENAL_BIN

**Métricas (Conjunto de Teste - 3.731 casos)**:
- Sensitivity (Recall): **43.64%**
- Specificity: **74.02%**
- NPV: **98.87%** ⭐
- AUC: **62.95%**

**Matriz de Confusão**:
- True Negatives: 2.721
- False Positives: 955
- False Negatives: 31
- True Positives: 24

---

## 💡 Como o Dashboard Funciona

### 1️⃣ Estatísticas Gerais
Mostra dados do **dataset REAL** (33.319 casos):
- Total de casos notificados
- Hospitalizações reais
- Distribuições por ano, sexo, idade, etc.

### 2️⃣ Predição do Modelo
Usa o **modelo treinado** para predizer:

**Entrada do Usuário** (5 sintomas):
- FEBRE
- MIALGIA
- CEFALEIA
- VOMITO
- EXANTEMA

**Processamento Interno**:
1. Calcula `SEVERITY_SCORE` baseado nos sintomas
2. Preenche outras 9 features com valores padrão:
   - DIAS_SINTOMA_NOTIFIC_TEMP: 2
   - TRIMESTRE: 1 (verão)
   - MES: 3 (março)
   - DIAS_SINTOMA_NOTIFIC: 2
   - TEM_COMORBIDADE: 0
   - NU_ANO: 2024
   - QTD_IGNORADOS: 0
   - IDADE: 35
   - ANO: 2024
   - HEPATOPAT_BIN: 0
   - COMORBIDADE_SCORE: 0
   - DIABETES_BIN: 0
   - RENAL_BIN: 0

3. Faz predição com as **14 features** completas

**Saída**:
- Probabilidade de hospitalização (0-100%)

---

## ⚠️ IMPORTANTE

### Por que mostrar 33 mil casos?

Os **33.319 casos** são os dados REAIS de Sertãozinho, usados para:
- ✅ Contextualizar o problema
- ✅ Mostrar a realidade epidemiológica local
- ✅ Análise exploratória de dados

### Por que o modelo foi balanceado?

O balanceamento (SMOTE) foi aplicado **APENAS** no conjunto de treino porque:
- Dataset real tem apenas 1.17% de hospitalizações (muito desbalanceado)
- Modelos não aprendem bem com classes desbalanceadas
- SMOTE cria casos sintéticos para balancear as classes
- Permite ao modelo aprender padrões da classe minoritária

### Qual é a versão correta?

✅ **DATASET**: 33.319 casos (df_dengue_tratado.csv) - CORRETO
✅ **MODELO**: modelo_reglog_otimizado.pkl - CORRETO
✅ **FEATURES**: 14 features - CORRETO
✅ **TREINAMENTO**: 15/11/2025 13:39:45 - MAIS RECENTE

---

## 🔍 Verificação Rápida

Para confirmar que está tudo correto:

```bash
cd /home/ericobon/insightesfera/PORTFOLIO_ACADEMICO/pi4v10/dashboard_dengue
python3 test_local.py
```

Deve mostrar:
- ✅ Dataset: 33,319 registros
- ✅ Modelo: LogisticRegression
- ✅ Features: 14
- ✅ Predição funcionando

---

**Tudo está correto! Os 33 mil casos são propositais - são os dados reais de Sertãozinho!** ✅
