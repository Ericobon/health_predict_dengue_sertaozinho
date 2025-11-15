#!/bin/bash

echo "======================================"
echo "Dashboard Dengue Sertãozinho"
echo "======================================"
echo ""

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
    echo "Ambiente virtual criado!"
    echo ""
fi

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
pip install -q -r requirements.txt

echo ""
echo "======================================"
echo "Iniciando aplicação..."
echo "======================================"
echo ""
echo "Acesse: http://localhost:5000"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

# Executar aplicação
python app.py
