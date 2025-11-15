#!/usr/bin/env python3
"""Script para testar o carregamento do modelo e predição localmente"""

import joblib
import pandas as pd
import numpy as np

print("="*60)
print("TESTE LOCAL - Dashboard Dengue")
print("="*60)

# 1. Testar carregamento do modelo
print("\n1. Carregando modelo...")
try:
    model = joblib.load("models/modelo_reglog_otimizado.pkl")
    print(f"   ✅ Modelo carregado: {type(model).__name__}")
except Exception as e:
    print(f"   ❌ ERRO: {e}")
    exit(1)

# 2. Testar carregamento do dataset
print("\n2. Carregando dataset...")
try:
    df = pd.read_csv("data/df_dengue_tratado.csv")
    print(f"   ✅ Dataset carregado: {len(df):,} registros")
except Exception as e:
    print(f"   ❌ ERRO: {e}")
    exit(1)

# 3. Testar predição
print("\n3. Testando predição...")
try:
    # Simular sintomas do usuário
    febre, mialgia, cefaleia, vomito, exantema = 1, 1, 1, 1, 1

    # Calcular severity
    severity = exantema * 1 + vomito * 3 + mialgia * 1 + cefaleia * 1 + febre * 1

    # Criar array com 14 features
    X_input = np.array([[
        2,          # DIAS_SINTOMA_NOTIFIC_TEMP
        1,          # TRIMESTRE
        3,          # MES
        2,          # DIAS_SINTOMA_NOTIFIC
        0,          # TEM_COMORBIDADE
        2024,       # NU_ANO
        0,          # QTD_IGNORADOS
        severity,   # SEVERITY_SCORE
        35,         # IDADE
        2024,       # ANO
        0,          # HEPATOPAT_BIN
        0,          # COMORBIDADE_SCORE
        0,          # DIABETES_BIN
        0           # RENAL_BIN
    ]])

    # Fazer predição
    prob = model.predict_proba(X_input)
    prob_hospitalização = prob[0][1] * 100

    print(f"   ✅ Predição realizada!")
    print(f"   📊 Probabilidade de hospitalização: {prob_hospitalização:.2f}%")

except Exception as e:
    print(f"   ❌ ERRO na predição: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "="*60)
print("✅ TODOS OS TESTES PASSARAM!")
print("="*60)
print("\nPara iniciar o dashboard:")
print("  python3 app.py")
print("\nDepois acesse: http://localhost:5000")
