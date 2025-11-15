# Guia de Deploy - Dashboard Dengue

## Opção 1: Render.com (Gratuito - RECOMENDADO)

### Passos:

1. **Criar conta no Render**: https://render.com

2. **Criar repositório Git**:
   ```bash
   cd /home/ericobon/insightesfera/PORTFOLIO_ACADEMICO/pi4v10/dashboard_dengue
   git init
   git add .
   git commit -m "Initial commit - Dashboard Dengue"
   ```

3. **Subir para GitHub**:
   ```bash
   # Criar repositório no GitHub primeiro
   git remote add origin https://github.com/SEU_USUARIO/dashboard-dengue.git
   git branch -M main
   git push -u origin main
   ```

4. **No Render**:
   - Clique em "New +" → "Web Service"
   - Conecte seu repositório GitHub
   - Configure:
     - **Name**: dashboard-dengue-sertaozinho
     - **Environment**: Python
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Instance Type**: Free
   - Clique em "Create Web Service"

5. **Aguarde o deploy** (3-5 minutos)

6. **Acesse**: `https://dashboard-dengue-sertaozinho.onrender.com`

---

## Opção 2: Railway.app (Gratuito)

### Passos:

1. **Criar conta**: https://railway.app

2. **Preparar repositório Git** (mesmo da opção 1)

3. **No Railway**:
   - Clique em "New Project" → "Deploy from GitHub repo"
   - Selecione seu repositório
   - Railway detecta automaticamente Python
   - Deploy automático!

4. **Configurar domínio**:
   - Settings → Generate Domain
   - Acesse o link gerado

---

## Opção 3: PythonAnywhere (Gratuito)

### Passos:

1. **Criar conta**: https://www.pythonanywhere.com

2. **Upload dos arquivos**:
   - Vá em "Files"
   - Upload todos os arquivos do projeto

3. **Configurar Web App**:
   - Web → Add a new web app
   - Choose "Flask"
   - Configure o WSGI file para apontar para `app.py`

4. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Reload** e acesse: `https://seuusuario.pythonanywhere.com`

---

## Opção 4: Compartilhamento Temporário (ngrok)

Para compartilhar **temporariamente** sem fazer deploy:

### Passos:

1. **Instalar ngrok**: https://ngrok.com/download

2. **Executar o dashboard**:
   ```bash
   python app.py
   ```

3. **Em outro terminal, executar ngrok**:
   ```bash
   ngrok http 5000
   ```

4. **Compartilhar o link** gerado (válido por 2 horas na versão gratuita)

---

## Opção 5: Vercel (Serverless)

Requer algumas modificações no código para funcionar como serverless.

---

## Recomendação

Para compartilhamento **permanente e gratuito**: **Render.com**
- Fácil configuração
- Deploy automático via Git
- SSL grátis
- Domínio .onrender.com
- Sempre online

Para compartilhamento **temporário**: **ngrok**
- Sem necessidade de criar conta
- Funciona imediatamente
- Link expira após algumas horas

---

## Troubleshooting

### Erro de memória no Render (Free tier)
Se o dataset for muito grande, considere:
- Reduzir o tamanho do CSV
- Usar amostragem dos dados
- Fazer cache dos gráficos

### Porta não configurada
Adicione ao `app.py`:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
```
