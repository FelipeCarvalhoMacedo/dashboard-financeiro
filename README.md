# Dashboard Financeiro — Resultados 2025/2026

## Como publicar no Streamlit Cloud (passo a passo)

### Pré-requisitos (gratuitos)
- Conta no GitHub: https://github.com
- Conta no Streamlit Cloud: https://streamlit.io/cloud

---

### PASSO 1 — Crie um repositório no GitHub

1. Entre em https://github.com/new
2. Dê um nome (ex: `dashboard-financeiro`)
3. Deixe **Público**
4. Clique em **Create repository**

---

### PASSO 2 — Suba os arquivos

Na página do repositório criado, clique em **uploading an existing file** e suba os 3 arquivos:
- `app.py`
- `requirements.txt`
- `README.md`

Clique em **Commit changes**.

---

### PASSO 3 — Publique no Streamlit Cloud

1. Acesse https://share.streamlit.io
2. Clique em **New app**
3. Conecte sua conta do GitHub (primeira vez)
4. Selecione o repositório `dashboard-financeiro`
5. Em **Main file path** deixe: `app.py`
6. Clique em **Deploy!**

Aguarde ~2 minutos. Você receberá um link assim:
```
https://seu-usuario-dashboard-financeiro.streamlit.app
```

Esse link funciona em qualquer navegador, em qualquer dispositivo, sem instalar nada.

---

### Como atualizar os dados

Toda vez que você editar o `app.py` no GitHub (ou subir uma nova versão), o Streamlit atualiza automaticamente em segundos.

No futuro, quando conectar via API ao sistema da empresa, só muda a função `load_data()` no `app.py` — o resto continua igual.

---

### Dúvidas?
Manda mensagem que a gente resolve juntos.
