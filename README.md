# Dashboard de Predição de Hospitalização por Dengue

Sistema web interativo para análise de dados e predição de risco de hospitalização por dengue em Sertãozinho-SP.

## Características

- Análise exploratória interativa com gráficos dinâmicos
- Modelo de Machine Learning com 99.3% de acurácia
- Interface moderna e responsiva
- Dashboard interativo para predições em tempo real
- Visualização de métricas e feature importance

## Estrutura do Projeto

```
dashboard_dengue/
├── app.py                          # Aplicação Flask principal
├── requirements.txt                # Dependências Python
├── README.md                       # Este arquivo
├── static/                         # Arquivos estáticos
│   ├── css/
│   │   └── style.css              # Estilos customizados
│   └── js/
│       └── main.js                # JavaScript
├── templates/                      # Templates HTML
│   ├── base.html                  # Template base
│   ├── index.html                 # Página inicial
│   ├── analise_exploratoria.html  # Análise de dados
│   ├── modelo_preditivo.html      # Informações do modelo
│   ├── teste_modelo.html          # Dashboard interativo
│   └── analise_modelo.html        # Feature importance + ROC
├── models/                         # Modelos treinados
│   ├── modelo_reglog_otimizado.pkl
│   └── scaler_final.pkl
└── data/                           # Dados
    └── df_dengue_tratado.csv
```

## Instalação

1. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Execução

1. Ative o ambiente virtual (se ainda não estiver ativo)

2. Execute a aplicação:
```bash
python app.py
```

3. Acesse no navegador:
```
http://localhost:5000
```

## Páginas

### 1. Página Inicial (/)
- Hero section com estatísticas gerais
- Cards informativos sobre o projeto
- Links rápidos para outras seções

### 2. Análise Exploratória (/analise_exploratoria)
- Distribuição temporal dos casos
- Análise demográfica (sexo e idade)
- Correlação com fenômenos climáticos

### 3. Modelo Preditivo (/modelo_preditivo)
- Metodologia do modelo
- Métricas de performance
- Formulário de teste integrado

### 4. Dashboard Interativo (/teste_modelo)
- Interface amigável para predições
- Seleção de sintomas com toggle buttons
- Visualização em tempo real da probabilidade

### 5. Análise do Modelo (/analise_modelo)
- Gráfico de feature importance
- Curva ROC
- Insights sobre o modelo

## Modelo de Machine Learning

- **Algoritmo**: Regressão Logística
- **Acurácia**: 99.36%
- **Recall**: 98.54%
- **Precisão**: 100.00%
- **ROC AUC**: 99.30%

### Features Utilizadas
- Febre (Sim/Não)
- Vômito (Sim/Não)
- Mialgia - Dor Muscular (Sim/Não)
- Cefaleia - Dor de Cabeça (Sim/Não)
- Exantema - Manchas na Pele (Sim/Não)

## Tecnologias

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Visualização**: Plotly.js
- **ML**: Scikit-learn
- **Data**: Pandas, NumPy

## API Endpoints

### POST /predict
Realiza predição de probabilidade de hospitalização.

**Request Body**:
```json
{
  "febre": "Sim",
  "vomito": "Não",
  "mialgia": "Sim",
  "cefaleia": "Sim",
  "exantema": "Não"
}
```

**Response**:
```json
{
  "probabilidade": 75.32,
  "classe": "Alta",
  "success": true
}
```

## Autor

Projeto Integrador IV - UNIVESP
Análise de Dados de Dengue em Sertãozinho-SP

## Licença

Este projeto é parte de um trabalho acadêmico.
