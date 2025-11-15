#!/bin/bash

echo "======================================"
echo "Deploy Dashboard Dengue para GitHub"
echo "======================================"
echo ""

# Verificar se está em um repositório git
if [ ! -d ".git" ]; then
    echo "Inicializando repositório Git..."
    git init
    echo ""
fi

# Adicionar todos os arquivos
echo "Adicionando arquivos ao Git..."
git add .

# Commit
echo ""
read -p "Digite a mensagem do commit (ou Enter para usar padrão): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Deploy: Dashboard de Predição de Dengue"
fi

git commit -m "$commit_msg"

# Verificar se já tem remote
if git remote | grep -q "origin"; then
    echo ""
    echo "Remote 'origin' já existe. Atualizando..."
    git push origin main
else
    echo ""
    echo "======================================"
    echo "Configuração do Remote"
    echo "======================================"
    echo ""
    echo "1. Crie um repositório no GitHub (https://github.com/new)"
    echo "2. NÃO inicialize com README, .gitignore ou license"
    echo ""
    read -p "Digite a URL do repositório (ex: https://github.com/usuario/repo.git): " repo_url

    git branch -M main
    git remote add origin "$repo_url"
    git push -u origin main
fi

echo ""
echo "======================================"
echo "Próximos Passos"
echo "======================================"
echo ""
echo "1. Acesse: https://render.com"
echo "2. Crie uma conta (pode usar GitHub)"
echo "3. Clique em 'New +' → 'Web Service'"
echo "4. Conecte seu repositório GitHub"
echo "5. Configure:"
echo "   - Name: dashboard-dengue-sertaozinho"
echo "   - Environment: Python"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn app:app"
echo "6. Clique em 'Create Web Service'"
echo ""
echo "Aguarde 3-5 minutos e seu dashboard estará online!"
echo ""
